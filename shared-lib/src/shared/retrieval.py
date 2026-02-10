"""Shared embedding store — embeds documents once and serves retrieval to all frameworks."""

from __future__ import annotations

from dataclasses import dataclass

import chromadb
from openai import OpenAI

from shared.interface import Document


@dataclass(frozen=True)
class RetrievalResult:
    """Chunks and source metadata returned from a retrieval query."""

    chunks: list[str]  # formatted as "[Source: file.md]\nchunk text..."
    sources: list[str]  # unique source file names


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping character-based chunks.

    This is the canonical chunking function.  Frameworks should import
    this instead of defining their own ``_chunk_text()``.
    """
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


class EmbeddingStore:
    """Embeds documents once, caches query embeddings, and serves retrieval.

    Designed to be instantiated once in the eval harness and shared across
    all framework evaluations for a given scenario run.

    Parameters
    ----------
    embedding_model:
        OpenAI embedding model name (e.g. ``"text-embedding-3-small"``).
    chunk_size:
        Character count per chunk.
    chunk_overlap:
        Overlap between consecutive chunks.
    top_k:
        Number of chunks to retrieve per query.
    """

    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 3,
    ) -> None:
        self._embedding_model = embedding_model
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._top_k = top_k

        self._openai_client: OpenAI | None = None
        self._chroma_client = chromadb.Client()
        self._collection: chromadb.Collection | None = None
        self._collection_name = "shared_embedding_store"
        self._ingested = False

        # Cache: question text → embedding vector
        self._query_cache: dict[str, list[float]] = {}

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def ingest(self, documents: list[Document]) -> None:
        """Chunk and embed all documents.  Idempotent — only embeds once."""
        if self._ingested:
            return

        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(
            name=self._collection_name,
        )

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_metadatas: list[dict] = []

        for doc in documents:
            chunks = chunk_text(doc.content, self._chunk_size, self._chunk_overlap)
            for i, text in enumerate(chunks):
                all_chunks.append(text)
                all_ids.append(f"{doc.source}_{i}")
                all_metadatas.append({"source": doc.source})

        response = openai_client.embeddings.create(
            model=self._embedding_model,
            input=all_chunks,
        )
        embeddings = [item.embedding for item in response.data]

        self._collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
        )
        self._ingested = True

    def retrieve(self, question: str, top_k: int | None = None) -> RetrievalResult:
        """Embed the question (with caching) and return top-k matching chunks."""
        if not self._ingested or self._collection is None:
            raise RuntimeError("Must call ingest() before retrieve()")

        k = top_k if top_k is not None else self._top_k

        # Cache the question embedding — reused across frameworks
        if question not in self._query_cache:
            openai_client = self._ensure_openai()
            response = openai_client.embeddings.create(
                model=self._embedding_model,
                input=question,
            )
            self._query_cache[question] = response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[self._query_cache[question]],
            n_results=k,
        )

        chunks: list[str] = []
        sources: list[str] = []
        if results["documents"] and results["documents"][0]:
            for doc_text, meta in zip(
                results["documents"][0], results["metadatas"][0]
            ):
                source = meta.get("source", "unknown")
                chunks.append(f"[Source: {source}]\n{doc_text}")
                if source not in sources:
                    sources.append(source)

        return RetrievalResult(chunks=chunks, sources=sources)

    def cleanup(self) -> None:
        """Release chromadb resources."""
        if self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
        self._ingested = False
        self._query_cache.clear()
