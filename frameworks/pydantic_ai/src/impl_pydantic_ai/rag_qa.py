"""Pydantic AI implementation of the RAG benchmark.

Uses a fixed retrieve→generate pipeline (same as LangGraph and smolagents)
to ensure a fair comparison. The retrieval step embeds the raw question and
fetches top-k chunks from chromadb. The generation step uses a Pydantic AI
Agent with the retrieved context injected into the prompt.
"""

from __future__ import annotations

import time
import uuid

import chromadb
from openai import OpenAI
from pydantic_ai import Agent

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, chunk_text

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

        # Step 1: Retrieve
        if self._embedding_store is not None:
            retrieval = self._embedding_store.retrieve(question)
            context_chunks = retrieval.chunks
            sources = retrieval.sources
        else:
            openai_client = self._ensure_openai()
            embed_response = openai_client.embeddings.create(
                model=EMBEDDING_MODEL, input=question
            )
            query_embedding = embed_response.data[0].embedding

            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=TOP_K,
            )

            context_chunks = []
            sources = []
            if results["documents"] and results["documents"][0]:
                for doc_text, meta in zip(
                    results["documents"][0], results["metadatas"][0]
                ):
                    source = meta.get("source", "unknown")
                    context_chunks.append(f"[Source: {source}]\n{doc_text}")
                    if source not in sources:
                        sources.append(source)

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
