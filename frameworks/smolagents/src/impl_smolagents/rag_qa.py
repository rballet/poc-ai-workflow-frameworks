"""smolagents implementation of the RAG benchmark."""

from __future__ import annotations

import asyncio
import time
import uuid
from functools import partial

import chromadb
from openai import OpenAI
from smolagents import CodeAgent, LiteLLMModel, Tool

from shared.interface import Answer, Document, RunResult, UsageStats

MODEL_ID = "openai/gpt-4o-mini"
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


class RetrieverTool(Tool):
    """Custom smolagents tool for semantic document retrieval."""

    name = "retriever"
    description = (
        "Uses semantic search to retrieve document chunks from the knowledge "
        "base that are most relevant to the query. Returns the top matching "
        "passages with their source document names."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": (
                "The search query to find relevant documents. "
                "Use affirmative form rather than a question."
            ),
        }
    }
    output_type = "string"

    def __init__(self, collection, openai_client, top_k=TOP_K, **kwargs):
        super().__init__(**kwargs)
        self.collection = collection
        self.openai_client = openai_client
        self.top_k = top_k

    def forward(self, query: str) -> str:
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL, input=query
        )
        query_embedding = response.data[0].embedding

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
        )

        if not results["documents"] or not results["documents"][0]:
            return "No relevant documents found."

        chunks = []
        for doc_text, meta in zip(
            results["documents"][0], results["metadatas"][0]
        ):
            source = meta.get("source", "unknown")
            chunks.append(f"[Source: {source}]\n{doc_text}")

        return "\nRetrieved documents:\n" + "\n\n---\n\n".join(chunks)


class SmolAgentsRAG:
    """RAGFramework implementation using smolagents."""

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
        """Answer a question using the smolagents RAG pipeline."""
        model = LiteLLMModel(model_id=self._model_id, temperature=0.1)
        retriever_tool = RetrieverTool(
            collection=self._collection,
            openai_client=self._ensure_openai(),
        )

        agent = CodeAgent(
            tools=[retriever_tool],
            model=model,
            max_steps=4,
            verbosity_level=0,
        )

        start = time.perf_counter()

        # smolagents is sync-only; run in a thread for async compatibility
        smol_result = await asyncio.to_thread(
            partial(agent.run, question, return_full_result=True)
        )

        elapsed = time.perf_counter() - start

        # Extract token usage
        input_tokens = 0
        output_tokens = 0
        if hasattr(smol_result, "token_usage") and smol_result.token_usage is not None:
            input_tokens = getattr(smol_result.token_usage, "input_tokens", 0) or 0
            output_tokens = getattr(smol_result.token_usage, "output_tokens", 0) or 0

        answer_text = str(smol_result.output) if smol_result.output else ""
        sources = self._extract_sources(agent)

        return RunResult(
            answer=Answer(
                question_id="",
                text=answer_text,
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

    def _extract_sources(self, agent) -> list[str]:
        """Extract unique source document names from agent memory."""
        sources = set()
        for step in agent.memory.steps:
            observations = getattr(step, "observations", "")
            if observations and "[Source:" in str(observations):
                for line in str(observations).split("\n"):
                    if "[Source:" in line:
                        source = line.split("[Source:")[1].split("]")[0].strip()
                        sources.add(source)
        return sorted(sources)

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
