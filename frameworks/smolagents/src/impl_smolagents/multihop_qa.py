"""smolagents implementation for the multihop_qa scenario."""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable

import chromadb
from openai import OpenAI
from smolagents import CodeAgent, LiteLLMModel, Tool

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

MODEL_ID = "openai/gpt-5-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

SYSTEM_PROMPT = (
    "You are a precise multi-hop RAG assistant. Use only tool-retrieved evidence. "
    "Cite source document names and avoid unsupported assumptions."
)


def _generate_sync(model: LiteLLMModel, system_prompt: str, user_message: str) -> dict:
    """Call the LLM synchronously via litellm (smolagents backend)."""
    import litellm

    comp_kwargs: dict = {
        "model": model.model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }
    if "gpt-5" not in model.model_id:
        comp_kwargs["temperature"] = 0
    response = litellm.completion(**comp_kwargs)
    choice = response.choices[0]
    usage = response.usage
    return {
        "answer": choice.message.content or "",
        "input_tokens": usage.prompt_tokens if usage else 0,
        "output_tokens": usage.completion_tokens if usage else 0,
    }


@dataclass
class RetrievalCall:
    query: str
    sources: list[str]
    chunks: list[str]


class RetrieverTool(Tool):
    """Tool used by CodeAgent for iterative retrieval."""

    name = "retrieve_context"
    description = (
        "Retrieve relevant evidence chunks for a query. Use this repeatedly to chain facts "
        "across documents (server -> rack -> datacenter -> SLA -> owner)."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "Focused retrieval query",
        },
    }
    output_type = "string"

    def __init__(
        self,
        retrieve_fn: Callable[[str, int], RetrievalResult],
        top_k: int,
        max_chunks_per_call: int,
        max_calls: int,
    ) -> None:
        super().__init__()
        self._retrieve_fn = retrieve_fn
        self._top_k = top_k
        self._max_chunks_per_call = max_chunks_per_call
        self._max_calls = max_calls
        self.calls: list[RetrievalCall] = []

    def forward(self, query: str) -> str:
        if len(self.calls) >= self._max_calls:
            return (
                "Budget exhausted: retrieval call limit reached. "
                "Proceed with already retrieved evidence."
            )

        retrieval = self._retrieve_fn(query, self._top_k)
        chunks = retrieval.chunks[: self._max_chunks_per_call]
        self.calls.append(
            RetrievalCall(
                query=query,
                sources=list(retrieval.sources),
                chunks=list(chunks),
            )
        )
        joined = "\n\n---\n\n".join(chunks)
        sources = ", ".join(retrieval.sources) if retrieval.sources else "None"
        return f"Sources: {sources}\n\n{joined}"


class SmolAgentsRAG:
    """RAGFramework implementation using native smolagents tool-based workflow."""

    def __init__(
        self,
        model_id: str = MODEL_ID,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model_id = model_id
        self._embedding_store = embedding_store
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"smolagents_multihop_{uuid.uuid4().hex[:8]}"

        self._mode = "baseline"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_agent_steps = 4
        self._max_retrieval_calls = 1

    @property
    def name(self) -> str:
        return "smolagents"

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
        default_steps = 2 if mode == "baseline" else int(mode_config.get("retrieval_rounds", 4)) + 2
        self._max_agent_steps = int(mode_config.get("max_steps", default_steps))
        default_calls = 1 if mode == "baseline" else int(mode_config.get("max_followup_queries", 4))
        self._max_retrieval_calls = int(mode_config.get("max_retrieval_calls", default_calls))

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _retrieve_once(self, query: str, top_k: int) -> RetrievalResult:
        if self._embedding_store is not None:
            return self._embedding_store.retrieve(query, top_k=top_k)

        openai_client = self._ensure_openai()
        embed_response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=query)
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

    def _capability_task_prompt(self, question: str) -> str:
        return (
            "Answer the question using iterative retrieval.\n"
            f"Question: {question}\n\n"
            "Rules:\n"
            f"- Use `retrieve_context` multiple times (up to {self._max_retrieval_calls} calls).\n"
            "- First query should be the original question.\n"
            "- Then issue focused follow-up queries for bridge facts (server, rack, datacenter, SLA, owner).\n"
            "- Do not assume missing facts; only use retrieved evidence.\n"
            "- Final answer must include source filenames.\n"
        )

    @staticmethod
    def _collect_trace(tool: RetrieverTool) -> tuple[list[str], list[str]]:
        query_trace: list[str] = []
        sources: list[str] = []
        for call in tool.calls:
            if len(query_trace) >= 100:
                break
            query_trace.append(call.query)
            for source in call.sources:
                if source not in sources:
                    sources.append(source)
        return query_trace, sources

    async def query(self, question: str) -> RunResult:
        """Answer question via baseline single-pass or native tool-driven capability mode."""
        start = time.perf_counter()

        model_kw: dict = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kw["temperature"] = 0
        model = LiteLLMModel(**model_kw)
        if self._mode == "baseline":
            retrieval = self._retrieve_once(question, self._top_k)
            context = "\n\n---\n\n".join(retrieval.chunks[: self._max_context_chunks])
            user_message = f"Context:\n{context}\n\nQuestion: {question}"

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
                    sources_used=retrieval.sources,
                    metadata={"mode": self._mode, "query_trace": [question]},
                ),
                usage=UsageStats(
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    latency_seconds=elapsed,
                    model_name=self._model_id,
                ),
            )

        retriever_tool = RetrieverTool(
            retrieve_fn=self._retrieve_once,
            top_k=self._top_k,
            max_chunks_per_call=max(1, self._max_context_chunks),
            max_calls=max(1, self._max_retrieval_calls),
        )
        agent = CodeAgent(
            tools=[retriever_tool],
            model=model,
            planning_interval=1,
            additional_authorized_imports=[],
            verbosity_level=0,
        )
        task_prompt = self._capability_task_prompt(question)

        run_result = await asyncio.to_thread(
            partial(
                agent.run,
                task_prompt,
                return_full_result=True,
                max_steps=self._max_agent_steps,
            )
        )
        elapsed = time.perf_counter() - start

        token_usage = run_result.token_usage
        input_tokens = token_usage.input_tokens if token_usage else 0
        output_tokens = token_usage.output_tokens if token_usage else 0
        total_tokens = token_usage.total_tokens if token_usage else (input_tokens + output_tokens)
        query_trace, sources = self._collect_trace(retriever_tool)

        return RunResult(
            answer=Answer(
                question_id="",
                text=str(run_result.output or ""),
                sources_used=sources,
                metadata={
                    "mode": self._mode,
                    "agent_state": str(run_result.state),
                    "query_trace": query_trace,
                    "retrieval_calls": len(retriever_tool.calls),
                },
            ),
            usage=UsageStats(
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                total_tokens=total_tokens,
                latency_seconds=elapsed,
                model_name=self._model_id,
            ),
        )

    async def cleanup(self) -> None:
        """Delete the chromadb collection."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
