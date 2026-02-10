"""Pydantic AI implementation for the multihop_qa scenario."""

from __future__ import annotations

import time
import uuid
from typing import Any

import chromadb
from openai import OpenAI
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

MODEL = "openai:gpt-4o-mini"
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
    "facts (entity mapping, ownership, location, SLA linkage)."
)

CHECKER_SYSTEM_PROMPT = (
    "Validate whether an answer fully supports a multi-hop question using the "
    "provided evidence summary. If not sufficient, suggest focused follow-up "
    "retrieval queries."
)


class QueryPlan(BaseModel):
    """Planned retrieval queries for a multi-hop question."""

    subqueries: list[str] = Field(default_factory=list)
    rationale: str = ""


class AnswerSufficiency(BaseModel):
    """Validation result for a drafted answer."""

    sufficient: bool = False
    missing_queries: list[str] = Field(default_factory=list)
    reasoning: str = ""


class PydanticAIRAG:
    """RAGFramework implementation using native Pydantic AI planning/validation."""

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
            self._collection_name = f"pydantic_ai_multihop_{uuid.uuid4().hex[:8]}"
        self._answer_agent: Agent[None, str] | None = None
        self._planner_agent: Agent[None, QueryPlan] | None = None
        self._checker_agent: Agent[None, AnswerSufficiency] | None = None

        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_plan_queries = 1
        self._max_validation_queries = 0

    @property
    def name(self) -> str:
        return "Pydantic AI"

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
        self._max_validation_queries = int(mode_config.get("max_validation_queries", 2 if mode == "capability" else 0))

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _ensure_answer_agent(self) -> Agent[None, str]:
        if self._answer_agent is None:
            self._answer_agent = Agent(
                self._model,
                output_type=str,
                instructions=ANSWER_SYSTEM_PROMPT,
            )
        return self._answer_agent

    def _ensure_planner_agent(self) -> Agent[None, QueryPlan]:
        if self._planner_agent is None:
            self._planner_agent = Agent(
                self._model,
                output_type=QueryPlan,
                instructions=PLANNER_SYSTEM_PROMPT,
            )
        return self._planner_agent

    def _ensure_checker_agent(self) -> Agent[None, AnswerSufficiency]:
        if self._checker_agent is None:
            self._checker_agent = Agent(
                self._model,
                output_type=AnswerSufficiency,
                instructions=CHECKER_SYSTEM_PROMPT,
            )
        return self._checker_agent

    @staticmethod
    def _usage_triplet(agent_result) -> tuple[int, int, int]:
        usage = agent_result.usage()
        in_tokens = usage.input_tokens or 0
        out_tokens = usage.output_tokens or 0
        total = usage.total_tokens or (in_tokens + out_tokens)
        return in_tokens, out_tokens, total

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

    async def ingest(self, documents: list[Document]) -> None:
        """Chunk documents, embed, and store in chromadb."""
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
        """Answer a question using baseline or native capability strategy."""
        answer_agent = self._ensure_answer_agent()
        start = time.perf_counter()

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        query_trace: list[str] = []
        chunks: list[str] = []
        sources: list[str] = []
        plan_output: QueryPlan | None = None
        check_output: AnswerSufficiency | None = None

        if self._mode == "baseline":
            self._retrieve_queries([question], 1, query_trace, chunks, sources)
            context = "\n\n---\n\n".join(chunks)
            answer_result = await answer_agent.run(
                f"Context:\n{context}\n\nQuestion: {question}"
            )
            in_t, out_t, tot_t = self._usage_triplet(answer_result)
            prompt_tokens += in_t
            completion_tokens += out_t
            total_tokens += tot_t
            final_answer = answer_result.output
        else:
            planner = self._ensure_planner_agent()
            checker = self._ensure_checker_agent()

            plan_result = await planner.run(
                "Question:\n"
                f"{question}\n\n"
                "Return focused retrieval subqueries that resolve intermediate facts."
            )
            plan_output = plan_result.output
            in_t, out_t, tot_t = self._usage_triplet(plan_result)
            prompt_tokens += in_t
            completion_tokens += out_t
            total_tokens += tot_t

            planned_queries = [q.strip() for q in plan_output.subqueries if q and q.strip()]
            if question not in planned_queries:
                planned_queries.insert(0, question)
            self._retrieve_queries(
                planned_queries,
                self._max_plan_queries,
                query_trace,
                chunks,
                sources,
            )

            context = "\n\n---\n\n".join(chunks)
            draft_result = await answer_agent.run(
                f"Context:\n{context}\n\nQuestion: {question}"
            )
            in_t, out_t, tot_t = self._usage_triplet(draft_result)
            prompt_tokens += in_t
            completion_tokens += out_t
            total_tokens += tot_t
            final_answer = draft_result.output

            check_result = await checker.run(
                "Question:\n"
                f"{question}\n\n"
                "Draft answer:\n"
                f"{final_answer}\n\n"
                "Sources used:\n"
                f"{', '.join(sources) if sources else 'None'}\n\n"
                "If not sufficient, provide follow-up retrieval queries."
            )
            check_output = check_result.output
            in_t, out_t, tot_t = self._usage_triplet(check_result)
            prompt_tokens += in_t
            completion_tokens += out_t
            total_tokens += tot_t

            if not check_output.sufficient and self._max_validation_queries > 0:
                self._retrieve_queries(
                    check_output.missing_queries,
                    self._max_validation_queries,
                    query_trace,
                    chunks,
                    sources,
                )
                context = "\n\n---\n\n".join(chunks)
                final_result = await answer_agent.run(
                    f"Context:\n{context}\n\nQuestion: {question}"
                )
                in_t, out_t, tot_t = self._usage_triplet(final_result)
                prompt_tokens += in_t
                completion_tokens += out_t
                total_tokens += tot_t
                final_answer = final_result.output

        elapsed = time.perf_counter() - start

        return RunResult(
            answer=Answer(
                question_id="",
                text=final_answer,
                sources_used=sources,
                metadata={
                    "mode": self._mode,
                    "query_trace": query_trace,
                    "plan": plan_output.model_dump() if plan_output is not None else None,
                    "validation": check_output.model_dump() if check_output is not None else None,
                },
            ),
            usage=UsageStats(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                latency_seconds=elapsed,
                model_name="gpt-4o-mini",
            ),
        )

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
