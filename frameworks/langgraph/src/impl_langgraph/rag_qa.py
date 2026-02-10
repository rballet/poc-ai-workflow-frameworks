"""LangGraph implementation of the RAG benchmark.

Uses a fixed retrieve→generate pipeline with a LangGraph StateGraph.
Same architecture as Pydantic AI and smolagents implementations for
fair comparison: embed raw question → retrieve top-k → generate with context.
"""

from __future__ import annotations

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

SYSTEM_PROMPT = (
    "You are a precise RAG assistant. Answer the question based ONLY on "
    "the provided context. Cite the source document names in your answer. "
    "If the context doesn't contain enough information to answer, say so."
)


class RAGState(TypedDict):
    """State for the RAG graph."""

    question: str
    context_chunks: list[str]
    context_sources: list[str]
    answer: str
    input_tokens: int
    output_tokens: int
    query_trace: list[str]


class LangGraphRAG:
    """RAGFramework implementation using LangGraph."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._graph = None
        # Only create chromadb/openai when running standalone; set None when using shared store
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"langgraph_{uuid.uuid4().hex[:8]}"
        else:
            self._chroma_client = None
            self._openai_client = None
            self._collection = None
            self._collection_name = None
        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K

    @property
    def name(self) -> str:
        return "LangGraph"

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def configure(
        self,
        *,
        mode: str,
        scenario_name: str,
        scenario_type: str,
        scenario_config: dict[str, Any],
        mode_config: dict[str, Any],
    ) -> None:
        """Configure runtime parameters for this scenario implementation."""
        _ = (scenario_name, scenario_type)
        self._mode = mode
        self._top_k = int(mode_config.get("top_k", scenario_config.get("top_k", TOP_K)))
        self._max_context_chunks = int(
            mode_config.get("max_context_chunks", self._top_k)
        )

    def _retrieve_once(self, query: str, top_k: int) -> RetrievalResult:
        """Retrieve top-k chunks for a single query from active store."""
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
        """Build the LangGraph StateGraph with retrieve and generate nodes."""
        model = self._model

        async def retrieve(state: RAGState) -> dict:
            """Embed the question and retrieve top-k chunks."""
            question = state["question"]
            retrieval_run = self._retrieve_once(question, top_k=self._top_k)
            return {
                "context_chunks": retrieval_run.chunks[: self._max_context_chunks],
                "context_sources": retrieval_run.sources,
                "query_trace": [question],
            }

        async def generate(state: RAGState) -> dict:
            """Call the LLM with retrieved context to generate an answer."""
            question = state["question"]
            context = "\n\n---\n\n".join(state["context_chunks"])

            llm = ChatOpenAI(model=model, temperature=0)
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=f"Context:\n{context}\n\nQuestion: {question}"
                ),
            ]

            response = await llm.ainvoke(messages)
            usage = response.usage_metadata or {}

            return {
                "answer": response.content,
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
            }

        workflow = StateGraph(RAGState)
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("generate", generate)
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    async def ingest(self, documents: list[Document]) -> None:
        """Chunk documents, embed, and store in chromadb."""
        if self._embedding_store is not None:
            self._graph = self._build_graph()
            return  # shared store already has the data

        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(
            name=self._collection_name
        )

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_metadatas: list[dict] = []

        for doc in documents:
            chunks = chunk_text(doc.content, CHUNK_SIZE, CHUNK_OVERLAP)
            for i, text in enumerate(chunks):
                all_chunks.append(text)
                all_ids.append(f"{doc.source}_{i}")
                all_metadatas.append({"source": doc.source})

        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=all_chunks
        )
        embeddings = [item.embedding for item in response.data]

        self._collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
        )

        self._graph = self._build_graph()

    async def query(self, question: str) -> RunResult:
        """Answer a question using the LangGraph RAG pipeline."""
        if self._graph is None:
            raise RuntimeError("Must call ingest() before query()")

        start = time.perf_counter()
        result = await self._graph.ainvoke(
            {
                "question": question,
                "context_chunks": [],
                "context_sources": [],
                "answer": "",
                "input_tokens": 0,
                "output_tokens": 0,
                "query_trace": [],
            }
        )
        elapsed = time.perf_counter() - start

        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)

        return RunResult(
            answer=Answer(
                question_id="",
                text=result["answer"],
                sources_used=result.get("context_sources", []),
                metadata={
                    "mode": self._mode,
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
