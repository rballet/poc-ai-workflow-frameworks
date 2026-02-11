"""Pydantic AI implementation for the agentic_sql_qa scenario."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from pydantic_ai import Agent, RunContext

from shared.agentic_sql import (
    LOOKUP_DOC_DESC,
    PROMPT_VERSION,
    RUN_SQL_DESC,
    AgenticSQLRuntime,
    build_task_prompt,
    get_system_prompt,
    get_system_prompt_hash,
)
from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore

MODEL = "openai:gpt-5-mini"
TOP_K = 4


@dataclass(frozen=True)
class AgentDeps:
    runtime: AgenticSQLRuntime


class PydanticAIRAG:
    """RAGFramework implementation using native Pydantic AI tools."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._agent: Agent[AgentDeps, str] | None = None
        self._runtime: AgenticSQLRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "agentic_sql_qa"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_tool_calls = 1

    @property
    def name(self) -> str:
        return "Pydantic AI"

    def configure(
        self,
        *,
        mode: str,
        scenario_name: str,
        scenario_type: str,
        scenario_config: dict[str, Any],
        mode_config: dict[str, Any],
    ) -> None:
        """Configure runtime parameters for agentic SQL QA."""
        _ = scenario_type
        self._mode = mode
        self._scenario_name = scenario_name
        self._database_seed_file = str(
            scenario_config.get("database_seed_file", "data/seed.sql")
        )
        self._top_k = int(mode_config.get("top_k", scenario_config.get("top_k", TOP_K)))
        self._max_context_chunks = int(
            mode_config.get("max_context_chunks", self._top_k)
        )
        default_calls = 1 if mode == "baseline" else 8
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_calls))

        if self._runtime is not None:
            self._runtime.set_limits(
                top_k=self._top_k,
                max_context_chunks=self._max_context_chunks,
            )

    def _ensure_agent(self) -> Agent[AgentDeps, str]:
        if self._agent is not None:
            return self._agent

        self._agent = Agent(
            self._model,
            output_type=str,
            instructions=get_system_prompt(),
            deps_type=AgentDeps,
        )

        @self._agent.tool(description=RUN_SQL_DESC)
        async def run_sql(ctx: RunContext[AgentDeps], query: str) -> str:
            """Execute read-only SQL on scenario data."""
            return ctx.deps.runtime.run_sql(query)

        @self._agent.tool(description=LOOKUP_DOC_DESC)
        async def lookup_doc(ctx: RunContext[AgentDeps], query: str) -> str:
            """Search scenario policy/process docs."""
            return ctx.deps.runtime.lookup_doc(query)

        return self._agent

    async def ingest(self, documents: list[Document]) -> None:
        """Prepare shared runtime resources."""
        self._runtime = AgenticSQLRuntime(
            scenario_name=self._scenario_name,
            database_seed_file=self._database_seed_file,
            embedding_store=self._embedding_store,
            top_k=self._top_k,
            max_context_chunks=self._max_context_chunks,
        )
        self._runtime.prepare(documents)

    async def query(self, question: str) -> RunResult:
        """Answer question through native Pydantic AI tool-calling."""
        if self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        agent = self._ensure_agent()
        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        prompt = build_task_prompt(question, self._max_tool_calls)

        start = time.perf_counter()
        result = await agent.run(
            prompt,
            deps=AgentDeps(runtime=self._runtime),
        )
        elapsed = time.perf_counter() - start

        usage = result.usage()
        prompt_tokens = usage.input_tokens or 0
        completion_tokens = usage.output_tokens or 0
        total_tokens = usage.total_tokens or (prompt_tokens + completion_tokens)

        trace = self._runtime.tool_trace()
        return RunResult(
            answer=Answer(
                question_id="",
                text=result.output,
                sources_used=self._runtime.sources_used(),
                metadata={
                    "mode": self._mode,
                    "prompt_version": PROMPT_VERSION,
                    "prompt_hash": get_system_prompt_hash(),
                    "tool_trace": trace,
                    "tool_calls": self._runtime.tool_calls(),
                    "query_trace": [str(item.get("input", "")) for item in trace],
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
        """Release runtime resources."""
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
