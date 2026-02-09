"""Pydantic AI implementation of the RAG benchmark."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

import chromadb
from openai import OpenAI
from pydantic_ai import Agent, RunContext

from shared.interface import Answer, Document, RunResult, UsageStats

MODEL = "openai:gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


@dataclass
class Deps:
    """Runtime dependencies for the RAG agent."""

    collection: chromadb.Collection | None = None
    openai_client: OpenAI | None = None
    source_map: dict[str, str] = field(default_factory=dict)


def _build_agent(model: str) -> Agent[Deps, str]:
    """Build the Pydantic AI agent with retrieval tool."""
    rag_agent = Agent(
        model,
        deps_type=Deps,
        output_type=str,
        instructions=(
            "You are a precise RAG assistant. Use the retrieve tool to find "
            "relevant documents, then answer the question based ONLY on the "
            "retrieved context. If the context doesn't contain the answer, "
            "say so. Cite the source document names."
        ),
    )

    @rag_agent.tool
    async def retrieve(context: RunContext[Deps], search_query: str) -> str:
        """Search the knowledge base for documents relevant to the query.

        Args:
            search_query: The search query to find relevant documents.
        """
        deps = context.deps
        if deps.collection is None or deps.openai_client is None:
            return "Knowledge base not initialized."

        response = deps.openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=search_query
        )
        query_embedding = response.data[0].embedding

        results = deps.collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K,
        )

        if not results["documents"] or not results["documents"][0]:
            return "No relevant documents found."

        chunks = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            source = meta.get("source", "unknown")
            chunks.append(f"[Source: {source}]\n{doc}")

        return "\n\n---\n\n".join(chunks)

    return rag_agent


class PydanticAIRAG:
    """RAGFramework implementation using Pydantic AI."""

    def __init__(self, model: str = MODEL) -> None:
        self._model = model
        self._agent: Agent[Deps, str] | None = None
        self._chroma_client = chromadb.Client()
        self._openai_client: OpenAI | None = None
        self._collection: chromadb.Collection | None = None
        self._collection_name = f"pydantic_ai_{uuid.uuid4().hex[:8]}"
        self._source_map: dict[str, str] = {}

    @property
    def name(self) -> str:
        return "Pydantic AI"

    def _ensure_agent(self) -> Agent[Deps, str]:
        if self._agent is None:
            self._agent = _build_agent(self._model)
        return self._agent

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
                self._source_map[chunk_id] = doc.source

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
        """Answer a question using the RAG pipeline."""
        agent = self._ensure_agent()
        deps = Deps(
            collection=self._collection,
            openai_client=self._ensure_openai(),
            source_map=self._source_map,
        )

        start = time.perf_counter()
        result = await agent.run(question, deps=deps)
        elapsed = time.perf_counter() - start

        usage = result.usage()
        sources_used = self._extract_sources(result)

        return RunResult(
            answer=Answer(
                question_id="",
                text=result.output,
                sources_used=sources_used,
            ),
            usage=UsageStats(
                prompt_tokens=usage.input_tokens or 0,
                completion_tokens=usage.output_tokens or 0,
                total_tokens=usage.total_tokens or 0,
                latency_seconds=elapsed,
                model_name="gpt-4o-mini",
            ),
        )

    def _extract_sources(self, result) -> list[str]:
        """Extract unique source document names from tool call results."""
        sources = set()
        for message in result.all_messages():
            msg_parts = getattr(message, "parts", [])
            for part in msg_parts:
                content = getattr(part, "content", "")
                if isinstance(content, str) and "[Source:" in content:
                    for line in content.split("\n"):
                        if line.startswith("[Source:"):
                            source = line.split("[Source:")[1].split("]")[0].strip()
                            sources.add(source)
        return sorted(sources)

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
