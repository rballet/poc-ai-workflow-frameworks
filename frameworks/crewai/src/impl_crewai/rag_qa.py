"""CrewAI implementation of the RAG benchmark.

Uses a fixed retrieve-then-generate pipeline (same as LangGraph, Pydantic AI,
and smolagents) to ensure a fair comparison. The retrieval step embeds the
raw question and fetches top-k chunks from the shared EmbeddingStore (or a
local chromadb collection). The generation step uses a CrewAI Agent/Task/Crew
with the retrieved context injected into the task description.
"""

from __future__ import annotations

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

SYSTEM_PROMPT = (
    "You are a precise RAG assistant. Answer the question based ONLY on "
    "the provided context. Cite the source document names in your answer. "
    "If the context doesn't contain enough information to answer, say so."
)


class CrewAIRAG:
    """RAGFramework implementation using CrewAI.

    Uses a fixed retrieve-then-generate pipeline for fair comparison.
    """

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        # Only create chromadb/openai when running standalone
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"crewai_{uuid.uuid4().hex[:8]}"
        self._agent: Agent | None = None
        self._llm: LLM | None = None
        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K

    @property
    def name(self) -> str:
        return "CrewAI"

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _ensure_agent(self) -> Agent:
        if self._agent is None:
            self._llm = LLM(model=self._model)
            self._agent = Agent(
                role="RAG Assistant",
                goal="Answer questions accurately based on provided context",
                backstory=SYSTEM_PROMPT,
                llm=self._llm,
                verbose=False,
            )
        return self._agent

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
        embed_response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=query,
        )
        query_embedding = embed_response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        context_chunks: list[str] = []
        sources: list[str] = []
        if results["documents"] and results["documents"][0]:
            for doc_text, meta in zip(results["documents"][0], results["metadatas"][0]):
                source = meta.get("source", "unknown")
                context_chunks.append(f"[Source: {source}]\n{doc_text}")
                if source not in sources:
                    sources.append(source)

        return RetrievalResult(chunks=context_chunks, sources=sources)

    async def ingest(self, documents: list[Document]) -> None:
        """Chunk documents, embed, and store in chromadb."""
        if self._embedding_store is not None:
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

    async def query(self, question: str) -> RunResult:
        """Answer a question using the fixed retrieve-then-generate pipeline."""
        agent = self._ensure_agent()

        start = time.perf_counter()

        retrieval = self._retrieve_once(question, self._top_k)
        context_chunks = retrieval.chunks[: self._max_context_chunks]
        sources = retrieval.sources

        context = "\n\n---\n\n".join(context_chunks)

        # Step 2: Generate — create a Task with context + question, run via Crew
        task = Task(
            description=f"Context:\n{context}\n\nQuestion: {question}",
            expected_output="A precise answer based on the provided context, citing source documents.",
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False,
        )

        result = await crew.kickoff_async()

        elapsed = time.perf_counter() - start

        # Extract token usage from CrewOutput (UsageMetrics pydantic model)
        token_usage = result.token_usage
        prompt_tokens = token_usage.prompt_tokens if token_usage else 0
        completion_tokens = token_usage.completion_tokens if token_usage else 0
        total_tokens = token_usage.total_tokens if token_usage else (prompt_tokens + completion_tokens)

        return RunResult(
            answer=Answer(
                question_id="",
                text=result.raw or "",
                sources_used=sources,
                metadata={
                    "mode": self._mode,
                    "query_trace": [question],
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
        """Delete the chromadb collection."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
