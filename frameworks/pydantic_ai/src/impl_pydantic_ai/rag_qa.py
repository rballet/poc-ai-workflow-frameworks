"""Pydantic AI implementation of the RAG benchmark.

Uses a fixed retrieve→generate pipeline (same as LangGraph and smolagents)
to ensure a fair comparison. The retrieval step embeds the raw question and
fetches top-k chunks from chromadb. The generation step uses a Pydantic AI
Agent with the retrieved context injected into the prompt.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

import chromadb
from openai import OpenAI
from pydantic_ai import Agent

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text
from shared.retrieval_strategy import (
    RetrievalStrategyConfig,
    iterative_retrieve,
)

MODEL = "openai:gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

SYSTEM_PROMPT = (
    "You are a precise RAG assistant. Answer the question based ONLY on "
    "the provided context. Cite the source document names in your answer. "
    "If the context doesn't contain enough information to answer, say so."
)


class PydanticAIRAG:
    """RAGFramework implementation using Pydantic AI.

    Uses a fixed retrieve→generate pipeline for fair comparison.
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
            self._collection_name = f"pydantic_ai_{uuid.uuid4().hex[:8]}"
        self._agent: Agent[None, str] | None = None
        self._mode = "baseline"
        self._strategy = RetrievalStrategyConfig()

    @property
    def name(self) -> str:
        return "Pydantic AI"

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _ensure_agent(self) -> Agent[None, str]:
        if self._agent is None:
            self._agent = Agent(
                self._model,
                output_type=str,
                instructions=SYSTEM_PROMPT,
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
        """Configure retrieval strategy per benchmark mode."""
        _ = (scenario_name, scenario_type)
        self._mode = mode
        top_k = int(mode_config.get("top_k", scenario_config.get("top_k", TOP_K)))
        rounds_default = 1 if mode == "baseline" else 3
        self._strategy = RetrievalStrategyConfig(
            top_k=top_k,
            retrieval_rounds=int(mode_config.get("retrieval_rounds", rounds_default)),
            max_context_chunks=int(mode_config.get("max_context_chunks", top_k)),
            max_followup_queries=int(mode_config.get("max_followup_queries", top_k)),
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
        """Answer a question using the fixed retrieve→generate pipeline."""
        agent = self._ensure_agent()

        start = time.perf_counter()

        # Step 1: Retrieve (baseline single-pass, capability iterative)
        retrieval_run = iterative_retrieve(
            question=question,
            retrieve_fn=self._retrieve_once,
            config=self._strategy,
        )
        context_chunks = retrieval_run.retrieval.chunks
        sources = retrieval_run.retrieval.sources

        context = "\n\n---\n\n".join(context_chunks)

        # Step 2: Generate — call agent with context + question
        user_message = f"Context:\n{context}\n\nQuestion: {question}"
        result = await agent.run(user_message)

        elapsed = time.perf_counter() - start

        usage = result.usage()

        return RunResult(
            answer=Answer(
                question_id="",
                text=result.output,
                sources_used=sources,
                metadata={
                    "mode": self._mode,
                    "query_trace": retrieval_run.query_trace,
                },
            ),
            usage=UsageStats(
                prompt_tokens=usage.input_tokens or 0,
                completion_tokens=usage.output_tokens or 0,
                total_tokens=usage.total_tokens or 0,
                latency_seconds=elapsed,
                model_name="gpt-4o-mini",
            ),
        )

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
