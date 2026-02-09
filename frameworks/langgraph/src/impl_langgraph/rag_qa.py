"""LangGraph implementation of the RAG benchmark."""

from __future__ import annotations

import operator
import time
import uuid
from typing import Annotated

import chromadb
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from typing_extensions import TypedDict

from shared.interface import Answer, Document, RunResult, UsageStats

MODEL = "gpt-4o-mini"
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


class RAGState(TypedDict):
    """State for the RAG graph."""

    question: str
    context_chunks: Annotated[list[str], operator.add]
    context_sources: Annotated[list[str], operator.add]
    answer: str
    input_tokens: int
    output_tokens: int


class LangGraphRAG:
    """RAGFramework implementation using LangGraph."""

    def __init__(self, model: str = MODEL) -> None:
        self._model = model
        self._chroma_client = chromadb.Client()
        self._openai_client: OpenAI | None = None
        self._collection: chromadb.Collection | None = None
        self._collection_name = f"langgraph_{uuid.uuid4().hex[:8]}"
        self._graph = None

    @property
    def name(self) -> str:
        return "LangGraph"

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _build_graph(self):
        """Build the LangGraph StateGraph with retrieve and generate nodes."""
        collection = self._collection
        openai_client = self._ensure_openai()
        model = self._model

        async def retrieve(state: RAGState) -> dict:
            """Embed the question and retrieve top-k chunks from chromadb."""
            question = state["question"]

            response = openai_client.embeddings.create(
                model=EMBEDDING_MODEL, input=question
            )
            query_embedding = response.data[0].embedding

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=TOP_K,
            )

            chunks = []
            sources = []
            if results["documents"] and results["documents"][0]:
                for doc, meta in zip(
                    results["documents"][0], results["metadatas"][0]
                ):
                    chunks.append(doc)
                    source = meta.get("source", "unknown")
                    if source not in sources:
                        sources.append(source)

            return {
                "context_chunks": chunks,
                "context_sources": sources,
            }

        async def generate(state: RAGState) -> dict:
            """Call the LLM with retrieved context to generate an answer."""
            question = state["question"]
            context = "\n\n---\n\n".join(state["context_chunks"])

            llm = ChatOpenAI(model=model, temperature=0)
            messages = [
                SystemMessage(
                    content=(
                        "You are a precise RAG assistant. Answer the question "
                        "based ONLY on the provided context. Cite the source "
                        "document names. If the context doesn't contain the "
                        "answer, say so."
                    )
                ),
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
        if self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
        self._graph = None
