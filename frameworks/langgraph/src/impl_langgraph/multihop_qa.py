"""LangGraph implementation for the multihop_qa scenario."""

from __future__ import annotations

import json
import re
import time
import uuid
from typing import Any

import chromadb
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from typing_extensions import TypedDict

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

ANSWER_SYSTEM_PROMPT = (
    "You are a precise multi-hop RAG assistant. Use only the provided context. "
    "Cite source document names in the answer. If key facts are missing, say so."
)

ASSESS_SYSTEM_PROMPT = (
    "Assess if current evidence is enough to answer a multi-hop question. "
    "Return JSON: {\"sufficient\": bool, \"next_queries\": [str], \"reason\": str}."
)


class RAGState(TypedDict):
    """State for iterative retrieval and answer generation."""

    question: str
    query_queue: list[str]
    seen_queries: list[str]
    query_trace: list[str]
    context_chunks: list[str]
    context_sources: list[str]
    steps: int
    should_stop: bool
    answer: str
    input_tokens: int
    output_tokens: int


class LangGraphRAG:
    """RAGFramework implementation using native LangGraph iterative workflow."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._graph = None
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"langgraph_multihop_{uuid.uuid4().hex[:8]}"
        else:
            self._chroma_client = None
            self._openai_client = None
            self._collection = None
            self._collection_name = None

        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_new_queries_per_step = 1

    @property
    def name(self) -> str:
        return "LangGraph"

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
        self._max_context_chunks = int(mode_config.get("max_context_chunks", self._top_k))
        default_steps = 1 if mode == "baseline" else int(mode_config.get("retrieval_rounds", 3))
        self._max_steps = int(mode_config.get("max_steps", default_steps))
        default_new_q = 1 if mode == "baseline" else int(mode_config.get("max_followup_queries", 3))
        self._max_new_queries_per_step = int(mode_config.get("max_new_queries_per_step", default_new_q))

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    @staticmethod
    def _merge_unique(existing: list[str], incoming: list[str], limit: int | None = None) -> list[str]:
        merged = list(existing)
        seen = set(existing)
        for item in incoming:
            if item not in seen:
                merged.append(item)
                seen.add(item)
            if limit is not None and len(merged) >= limit:
                break
        return merged

    @staticmethod
    def _seed_queries(question: str) -> list[str]:
        seeds = [question.strip()]
        lowered = question.lower()
        if "datacenter" in lowered:
            seeds.append(f"{question} rack mapping")
        if "uptime" in lowered or "sla" in lowered:
            seeds.append(f"{question} region SLA tier")
        return [q for q in seeds if q]

    @staticmethod
    def _derive_queries_from_context(chunks: list[str], limit: int) -> list[str]:
        text = "\n".join(chunks)
        queries: list[str] = []
        for server in re.findall(r"\bprod-api-\d{2}\b", text, flags=re.IGNORECASE):
            queries.append(f"{server.lower()} project rack datacenter")
        for rack in re.findall(r"\bR-\d{3}\b", text, flags=re.IGNORECASE):
            queries.append(f"{rack.upper()} datacenter rack range")
        for incident in re.findall(r"\bINC-\d{4}-\d{3}\b", text, flags=re.IGNORECASE):
            queries.append(f"{incident.upper()} affected server owner")
        deduped: list[str] = []
        seen: set[str] = set()
        for query in queries:
            key = query.lower()
            if key not in seen:
                seen.add(key)
                deduped.append(query)
            if len(deduped) >= limit:
                break
        return deduped

    @staticmethod
    def _parse_assessment(content: str) -> tuple[bool, list[str]]:
        try:
            data = json.loads(content)
            sufficient = bool(data.get("sufficient", False))
            next_queries = data.get("next_queries", [])
            if not isinstance(next_queries, list):
                next_queries = []
            clean_queries = [str(q).strip() for q in next_queries if str(q).strip()]
            return sufficient, clean_queries
        except Exception:
            return False, []

    def _retrieve_once(self, query: str, top_k: int) -> RetrievalResult:
        if self._embedding_store is not None:
            return self._embedding_store.retrieve(query, top_k=top_k)

        openai_client = self._ensure_openai()
        response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=query)
        query_embedding = response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        chunks: list[str] = []
        sources: list[str] = []
        if results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                source = meta.get("source", "unknown")
                chunks.append(f"[Source: {source}]\n{doc}")
                if source not in sources:
                    sources.append(source)
        return RetrievalResult(chunks=chunks, sources=sources)

    def _build_graph(self):
        """Build iterative retrieve-assess-generate workflow."""
        model = self._model
        top_k = self._top_k
        max_steps = self._max_steps
        max_context = self._max_context_chunks
        max_new_queries = self._max_new_queries_per_step

        async def retrieve(state: RAGState) -> dict:
            queue = list(state["query_queue"])
            if not queue:
                return {"should_stop": True}

            query = queue.pop(0)
            retrieval = self._retrieve_once(query, top_k)
            context_chunks = self._merge_unique(
                state["context_chunks"], retrieval.chunks, limit=max_context
            )
            context_sources = self._merge_unique(state["context_sources"], retrieval.sources)
            seen_queries = self._merge_unique(state["seen_queries"], [query])
            query_trace = self._merge_unique(state["query_trace"], [query])

            return {
                "query_queue": queue,
                "seen_queries": seen_queries,
                "query_trace": query_trace,
                "context_chunks": context_chunks,
                "context_sources": context_sources,
                "steps": state["steps"] + 1,
            }

        async def assess(state: RAGState) -> dict:
            # Baseline mode: one retrieval pass then generate immediately.
            if self._mode == "baseline":
                return {"should_stop": True}

            if state["steps"] >= max_steps:
                return {"should_stop": True}

            llm = ChatOpenAI(model=model, temperature=0)
            context_preview = "\n\n---\n\n".join(state["context_chunks"])
            messages = [
                SystemMessage(content=ASSESS_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"Question:\n{state['question']}\n\n"
                        f"Evidence:\n{context_preview}\n\n"
                        f"Seen queries: {state['seen_queries']}"
                    )
                ),
            ]
            response = await llm.ainvoke(messages)
            usage = response.usage_metadata or {}
            sufficient, llm_queries = self._parse_assessment(str(response.content))
            heuristic_queries = self._derive_queries_from_context(
                state["context_chunks"], limit=max_new_queries
            )

            candidates = llm_queries + heuristic_queries
            unseen: list[str] = []
            seen = {q.lower() for q in state["seen_queries"]}
            for query in candidates:
                key = query.lower()
                if key not in seen:
                    unseen.append(query)
                    seen.add(key)
                if len(unseen) >= max_new_queries:
                    break

            queue = self._merge_unique(state["query_queue"], unseen)
            should_stop = sufficient or not queue or state["steps"] >= max_steps

            return {
                "query_queue": queue,
                "should_stop": should_stop,
                "input_tokens": state["input_tokens"] + usage.get("input_tokens", 0),
                "output_tokens": state["output_tokens"] + usage.get("output_tokens", 0),
            }

        async def generate(state: RAGState) -> dict:
            context = "\n\n---\n\n".join(state["context_chunks"])
            llm = ChatOpenAI(model=model, temperature=0)
            messages = [
                SystemMessage(content=ANSWER_SYSTEM_PROMPT),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {state['question']}"),
            ]
            response = await llm.ainvoke(messages)
            usage = response.usage_metadata or {}
            return {
                "answer": str(response.content),
                "input_tokens": state["input_tokens"] + usage.get("input_tokens", 0),
                "output_tokens": state["output_tokens"] + usage.get("output_tokens", 0),
            }

        def route_from_assess(state: RAGState) -> str:
            return "generate" if state["should_stop"] else "retrieve"

        workflow = StateGraph(RAGState)
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("assess", assess)
        workflow.add_node("generate", generate)
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "assess")
        workflow.add_conditional_edges(
            "assess",
            route_from_assess,
            path_map={"retrieve": "retrieve", "generate": "generate"},
        )
        workflow.add_edge("generate", END)
        return workflow.compile()

    async def ingest(self, documents: list[Document]) -> None:
        """Chunk documents, embed, and store in chromadb."""
        if self._embedding_store is not None:
            self._graph = self._build_graph()
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
        self._graph = self._build_graph()

    async def query(self, question: str) -> RunResult:
        """Answer a question with iterative LangGraph orchestration."""
        if self._graph is None:
            raise RuntimeError("Must call ingest() before query()")

        start = time.perf_counter()
        result = await self._graph.ainvoke(
            {
                "question": question,
                "query_queue": self._seed_queries(question),
                "seen_queries": [],
                "query_trace": [],
                "context_chunks": [],
                "context_sources": [],
                "steps": 0,
                "should_stop": False,
                "answer": "",
                "input_tokens": 0,
                "output_tokens": 0,
            }
        )
        elapsed = time.perf_counter() - start

        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)

        return RunResult(
            answer=Answer(
                question_id="",
                text=result.get("answer", ""),
                sources_used=result.get("context_sources", []),
                metadata={
                    "mode": self._mode,
                    "steps": result.get("steps", 0),
                    "query_trace": result.get("query_trace", []),
                },
            ),
            usage=UsageStats(
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                latency_seconds=elapsed,
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
        self._graph = None
