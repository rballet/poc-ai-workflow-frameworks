"""CrewAI implementation for the multihop_qa scenario.

Baseline mode: single retrieval pass then generate answer.
Capability mode: iterative retrieval with planning and sufficiency checking
using separate CrewAI agents for planning, answering, and validation.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

import chromadb
from crewai import Agent, Crew, LLM, Task
from openai import OpenAI

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

MODEL = "openai/gpt-5-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

ANSWER_SYSTEM_PROMPT = (
    "You are a precise multi-hop RAG assistant. Build the answer from retrieved "
    "evidence only. If evidence is insufficient, say exactly what is missing. "
    "Always cite source document names."
)

PLANNER_SYSTEM_PROMPT = (
    "Generate concise retrieval subqueries for multi-hop QA. Prioritize bridge "
    "facts (entity mapping, ownership, location, SLA linkage). "
    "Return ONLY valid JSON: {\"subqueries\": [\"query1\", \"query2\", ...], \"rationale\": \"...\"}"
)

CHECKER_SYSTEM_PROMPT = (
    "Validate whether an answer fully supports a multi-hop question using the "
    "provided evidence summary. If not sufficient, suggest focused follow-up "
    "retrieval queries. "
    "Return ONLY valid JSON: {\"sufficient\": true/false, \"missing_queries\": [\"q1\", ...], \"reasoning\": \"...\"}"
)


def _parse_json_from_text(text: str) -> dict:
    """Extract JSON from a text response that may contain extra content."""
    text = text.strip()
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try to find JSON block in markdown code fences
    for marker_start, marker_end in [("```json", "```"), ("```", "```"), ("{", None)]:
        idx = text.find(marker_start)
        if idx == -1:
            continue
        if marker_end and marker_start != "{":
            start = idx + len(marker_start)
            end = text.find(marker_end, start)
            candidate = text[start:end].strip() if end != -1 else text[start:].strip()
        else:
            # Find matching closing brace
            candidate = text[idx:]
            brace_count = 0
            for i, ch in enumerate(candidate):
                if ch == "{":
                    brace_count += 1
                elif ch == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        candidate = candidate[: i + 1]
                        break
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return {}


class CrewAIRAG:
    """RAGFramework implementation using CrewAI for multihop QA."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"crewai_multihop_{uuid.uuid4().hex[:8]}"
        self._llm: LLM | None = None
        self._answer_agent: Agent | None = None
        self._planner_agent: Agent | None = None
        self._checker_agent: Agent | None = None

        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_plan_queries = 1
        self._max_validation_queries = 0

    @property
    def name(self) -> str:
        return "CrewAI"

    def configure(
        self,
        *,
        mode: str,
        scenario_name: str,
        scenario_type: str,
        scenario_config: dict[str, Any],
        mode_config: dict[str, Any],
    ) -> None:
        """Configure baseline/capability strategy for multihop QA."""
        _ = (scenario_name, scenario_type)
        self._mode = mode
        self._top_k = int(mode_config.get("top_k", scenario_config.get("top_k", TOP_K)))
        default_plan_queries = 1 if mode == "baseline" else int(mode_config.get("retrieval_rounds", 3))
        self._max_plan_queries = int(mode_config.get("max_plan_queries", default_plan_queries))
        self._max_context_chunks = int(mode_config.get("max_context_chunks", self._top_k))
        self._max_validation_queries = int(
            mode_config.get("max_validation_queries", 2 if mode == "capability" else 0)
        )

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _ensure_llm(self) -> LLM:
        if self._llm is None:
            self._llm = LLM(model=self._model)
        return self._llm

    def _ensure_answer_agent(self) -> Agent:
        if self._answer_agent is None:
            self._answer_agent = Agent(
                role="RAG Answer Agent",
                goal="Answer questions accurately based on provided context",
                backstory=ANSWER_SYSTEM_PROMPT,
                llm=self._ensure_llm(),
                verbose=False,
            )
        return self._answer_agent

    def _ensure_planner_agent(self) -> Agent:
        if self._planner_agent is None:
            self._planner_agent = Agent(
                role="Query Planner",
                goal="Generate focused retrieval subqueries for multi-hop questions",
                backstory=PLANNER_SYSTEM_PROMPT,
                llm=self._ensure_llm(),
                verbose=False,
            )
        return self._planner_agent

    def _ensure_checker_agent(self) -> Agent:
        if self._checker_agent is None:
            self._checker_agent = Agent(
                role="Answer Validator",
                goal="Validate answer sufficiency and suggest follow-up queries",
                backstory=CHECKER_SYSTEM_PROMPT,
                llm=self._ensure_llm(),
                verbose=False,
            )
        return self._checker_agent

    def _retrieve_once(self, query: str, top_k: int) -> RetrievalResult:
        if self._embedding_store is not None:
            return self._embedding_store.retrieve(query, top_k=top_k)

        openai_client = self._ensure_openai()
        embed_response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=query)
        query_embedding = embed_response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        chunks: list[str] = []
        sources: list[str] = []
        if results["documents"] and results["documents"][0]:
            for doc_text, meta in zip(results["documents"][0], results["metadatas"][0]):
                source = meta.get("source", "unknown")
                chunks.append(f"[Source: {source}]\n{doc_text}")
                if source not in sources:
                    sources.append(source)
        return RetrievalResult(chunks=chunks, sources=sources)

    def _retrieve_queries(
        self,
        queries: list[str],
        max_queries: int,
        query_trace: list[str],
        chunks: list[str],
        sources: list[str],
    ) -> None:
        seen_chunks = set(chunks)
        for query in queries[:max_queries]:
            cleaned = query.strip()
            if not cleaned:
                continue
            retrieval = self._retrieve_once(cleaned, self._top_k)
            query_trace.append(cleaned)
            for chunk in retrieval.chunks:
                if chunk not in seen_chunks and len(chunks) < self._max_context_chunks:
                    seen_chunks.add(chunk)
                    chunks.append(chunk)
            for source in retrieval.sources:
                if source not in sources:
                    sources.append(source)

    @staticmethod
    def _extract_tokens(result) -> tuple[int, int, int]:
        """Extract token counts from a CrewOutput's UsageMetrics."""
        tu = result.token_usage
        if tu is None:
            return 0, 0, 0
        return tu.prompt_tokens, tu.completion_tokens, tu.total_tokens

    async def _run_crew(self, agent: Agent, description: str, expected_output: str):
        """Run a single-agent Crew and return the CrewOutput."""
        task = Task(description=description, expected_output=expected_output, agent=agent)
        crew = Crew(agents=[agent], tasks=[task], verbose=False)
        return await crew.kickoff_async()

    async def ingest(self, documents: list[Document]) -> None:
        if self._embedding_store is not None:
            return

        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(name=self._collection_name)

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_metadatas: list[dict] = []

        for doc in documents:
            chunks = chunk_text(doc.content, CHUNK_SIZE, CHUNK_OVERLAP)
            for i, text in enumerate(chunks):
                all_chunks.append(text)
                all_ids.append(f"{doc.source}_{i}")
                all_metadatas.append({"source": doc.source})

        response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=all_chunks)
        embeddings = [item.embedding for item in response.data]

        self._collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
        )

    async def query(self, question: str) -> RunResult:
        """Answer a question using baseline or capability strategy."""
        start = time.perf_counter()

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        query_trace: list[str] = []
        chunks: list[str] = []
        sources: list[str] = []
        plan_data: dict | None = None
        check_data: dict | None = None

        if self._mode == "baseline":
            # Single retrieval pass + generate
            self._retrieve_queries([question], 1, query_trace, chunks, sources)
            context = "\n\n---\n\n".join(chunks)

            result = await self._run_crew(
                self._ensure_answer_agent(),
                f"Context:\n{context}\n\nQuestion: {question}",
                "A precise answer based on the provided context, citing source documents.",
            )
            pt, ct, tt = self._extract_tokens(result)
            prompt_tokens += pt
            completion_tokens += ct
            total_tokens += tt
            final_answer = result.raw or ""
        else:
            # Step 1: Plan subqueries
            plan_result = await self._run_crew(
                self._ensure_planner_agent(),
                (
                    f"Question:\n{question}\n\n"
                    "Return focused retrieval subqueries that resolve intermediate facts. "
                    "Output ONLY valid JSON: {\"subqueries\": [...], \"rationale\": \"...\"}"
                ),
                "A JSON object with subqueries and rationale.",
            )
            pt, ct, tt = self._extract_tokens(plan_result)
            prompt_tokens += pt
            completion_tokens += ct
            total_tokens += tt

            plan_data = _parse_json_from_text(plan_result.raw or "")
            planned_queries = [q.strip() for q in plan_data.get("subqueries", []) if q and q.strip()]
            if question not in planned_queries:
                planned_queries.insert(0, question)

            # Step 2: Retrieve for planned queries
            self._retrieve_queries(planned_queries, self._max_plan_queries, query_trace, chunks, sources)

            # Step 3: Generate draft answer
            context = "\n\n---\n\n".join(chunks)
            draft_result = await self._run_crew(
                self._ensure_answer_agent(),
                f"Context:\n{context}\n\nQuestion: {question}",
                "A precise answer based on the provided context, citing source documents.",
            )
            pt, ct, tt = self._extract_tokens(draft_result)
            prompt_tokens += pt
            completion_tokens += ct
            total_tokens += tt
            final_answer = draft_result.raw or ""

            # Step 4: Check sufficiency
            check_result = await self._run_crew(
                self._ensure_checker_agent(),
                (
                    f"Question:\n{question}\n\n"
                    f"Draft answer:\n{final_answer}\n\n"
                    f"Sources used:\n{', '.join(sources) if sources else 'None'}\n\n"
                    "If not sufficient, provide follow-up retrieval queries. "
                    "Output ONLY valid JSON: {\"sufficient\": true/false, \"missing_queries\": [...], \"reasoning\": \"...\"}"
                ),
                "A JSON object with sufficient flag and optional missing queries.",
            )
            pt, ct, tt = self._extract_tokens(check_result)
            prompt_tokens += pt
            completion_tokens += ct
            total_tokens += tt

            check_data = _parse_json_from_text(check_result.raw or "")
            is_sufficient = check_data.get("sufficient", False)

            # Step 5: If not sufficient, retrieve more and re-generate
            if not is_sufficient and self._max_validation_queries > 0:
                missing_queries = [q.strip() for q in check_data.get("missing_queries", []) if q and q.strip()]
                self._retrieve_queries(missing_queries, self._max_validation_queries, query_trace, chunks, sources)

                context = "\n\n---\n\n".join(chunks)
                final_result = await self._run_crew(
                    self._ensure_answer_agent(),
                    f"Context:\n{context}\n\nQuestion: {question}",
                    "A precise answer based on the provided context, citing source documents.",
                )
                pt, ct, tt = self._extract_tokens(final_result)
                prompt_tokens += pt
                completion_tokens += ct
                total_tokens += tt
                final_answer = final_result.raw or ""

        elapsed = time.perf_counter() - start

        return RunResult(
            answer=Answer(
                question_id="",
                text=final_answer,
                sources_used=sources,
                metadata={
                    "mode": self._mode,
                    "query_trace": query_trace,
                    "plan": plan_data,
                    "validation": check_data,
                },
            ),
            usage=UsageStats(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                latency_seconds=elapsed,
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
