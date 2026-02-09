"""smolagents implementation of the RAG benchmark.

Uses a fixed retrieve→generate pipeline (same as LangGraph and Pydantic AI)
to ensure a fair comparison. The retrieval step embeds the raw question and
fetches top-k chunks from chromadb. The generation step uses a smolagents
LiteLLMModel directly (no CodeAgent) with the retrieved context.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from functools import partial

import chromadb
from openai import OpenAI
from smolagents import LiteLLMModel

from shared.interface import Answer, Document, RunResult, UsageStats

MODEL_ID = "openai/gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

SYSTEM_PROMPT = (
    "You are a precise RAG assistant. Answer the question based ONLY on "
    "the provided context. Cite the source document names in your answer. "
    "If the context doesn't contain enough information to answer, say so."
)


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def _generate_sync(model: LiteLLMModel, system_prompt: str, user_message: str) -> dict:
    """Call the LLM synchronously via smolagents' LiteLLMModel."""
    import litellm

    response = litellm.completion(
        model=model.model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    choice = response.choices[0]
    usage = response.usage

    return {
        "answer": choice.message.content or "",
        "input_tokens": usage.prompt_tokens if usage else 0,
        "output_tokens": usage.completion_tokens if usage else 0,
    }


class SmolAgentsRAG:
    """RAGFramework implementation using smolagents.

    Uses a fixed retrieve→generate pipeline for fair comparison.
    """

    def __init__(self, model_id: str = MODEL_ID) -> None:
        self._model_id = model_id
        self._chroma_client = chromadb.Client()
        self._openai_client: OpenAI | None = None
        self._collection: chromadb.Collection | None = None
        self._collection_name = f"smolagents_{uuid.uuid4().hex[:8]}"

    @property
    def name(self) -> str:
        return "smolagents"

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    async def ingest(self, documents: list[Document]) -> None:
        """Chunk documents, embed, and store in chromadb."""
        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(
            name=self._collection_name
        )

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_metadatas: list[dict] = []

        for doc in documents:
            chunks = _chunk_text(doc.content, CHUNK_SIZE, CHUNK_OVERLAP)
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc.source}_{i}"
                all_chunks.append(chunk)
                all_ids.append(chunk_id)
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
        openai_client = self._ensure_openai()
        model = LiteLLMModel(model_id=self._model_id, temperature=0)

        start = time.perf_counter()

        # Step 1: Retrieve — embed the raw question, search chromadb
        embed_response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=question
        )
        query_embedding = embed_response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K,
        )

        # Extract chunks and sources
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
        user_message = f"Context:\n{context}\n\nQuestion: {question}"

        # Step 2: Generate — call LLM via litellm (smolagents' backend)
        # smolagents is sync-only, so we bridge to async
        gen_result = await asyncio.to_thread(
            partial(_generate_sync, model, SYSTEM_PROMPT, user_message)
        )

        elapsed = time.perf_counter() - start

        input_tokens = gen_result.get("input_tokens", 0)
        output_tokens = gen_result.get("output_tokens", 0)

        return RunResult(
            answer=Answer(
                question_id="",
                text=gen_result["answer"],
                sources_used=sources,
            ),
            usage=UsageStats(
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                latency_seconds=elapsed,
                model_name=self._model_id,
            ),
        )

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
