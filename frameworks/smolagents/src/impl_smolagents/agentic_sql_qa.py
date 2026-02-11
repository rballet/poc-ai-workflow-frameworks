"""smolagents implementation for the agentic_sql_qa scenario."""

from __future__ import annotations

import asyncio
import threading
import time
from functools import partial
from typing import Any

from smolagents import LiteLLMModel, Tool, ToolCallingAgent

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

MODEL_ID = "openai/gpt-5-mini"
TOP_K = 4


class SQLTool(Tool):
    """Execute read-only SQL on the shared scenario runtime."""

    name = "run_sql"
    description = RUN_SQL_DESC
    inputs = {
        "query": {"type": "string", "description": "SQL query to execute"},
    }
    output_type = "string"

    def __init__(self, runtime: AgenticSQLRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.run_sql(query)


class DocTool(Tool):
    """Search policy/process docs on the shared scenario runtime."""

    name = "lookup_doc"
    description = LOOKUP_DOC_DESC
    inputs = {
        "query": {"type": "string", "description": "Search query"},
    }
    output_type = "string"

    def __init__(self, runtime: AgenticSQLRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.lookup_doc(query)


class SmolAgentsRAG:
    """RAGFramework implementation using native smolagents tool-calling."""

    def __init__(
        self,
        model_id: str = MODEL_ID,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model_id = model_id
        self._embedding_store = embedding_store
        self._runtime: AgenticSQLRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "agentic_sql_qa"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 1
        self._planning_interval: int | None = None

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
        default_steps = 1 if mode == "baseline" else 8
        self._max_steps = int(mode_config.get("max_steps", default_steps))
        default_calls = 1 if mode == "baseline" else 8
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_calls))
        default_planning_interval: int | None = None if mode == "baseline" else 1
        planning_interval = mode_config.get("planning_interval", default_planning_interval)
        self._planning_interval = (
            None
            if planning_interval is None
            else int(planning_interval)
        )

        if self._runtime is not None:
            self._runtime.set_limits(
                top_k=self._top_k,
                max_context_chunks=self._max_context_chunks,
            )

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
        """Answer question through native smolagents ToolCallingAgent."""
        if self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)
        agent = ToolCallingAgent(
            tools=[SQLTool(self._runtime), DocTool(self._runtime)],
            model=model,
            instructions=get_system_prompt(),
            planning_interval=self._planning_interval,
            max_steps=self._max_steps,
            verbosity_level=0,
        )

        task = build_task_prompt(question, self._max_tool_calls)

        # Use a timer to interrupt the agent if it exceeds the timeout.
        # asyncio.wait_for() cannot cancel threads spawned by to_thread(),
        # so we use smolagents' native interrupt_switch mechanism.
        timeout_seconds = 120.0
        timer = threading.Timer(timeout_seconds, agent.interrupt)
        timer.start()

        start = time.perf_counter()
        try:
            run_result = await asyncio.to_thread(
                partial(
                    agent.run,
                    task,
                    max_steps=self._max_steps,
                    return_full_result=True,
                )
            )
        except Exception:
            elapsed = time.perf_counter() - start
            trace = self._runtime.tool_trace()
            return RunResult(
                answer=Answer(
                    question_id="",
                    text="Agent timed out or was interrupted before producing an answer.",
                    sources_used=self._runtime.sources_used(),
                    metadata={
                        "mode": self._mode,
                        "prompt_version": PROMPT_VERSION,
                        "prompt_hash": get_system_prompt_hash(),
                        "agent_state": "interrupted",
                        "planning_interval": self._planning_interval,
                        "tool_trace": trace,
                        "tool_calls": self._runtime.tool_calls(),
                        "query_trace": [str(item.get("input", "")) for item in trace],
                    },
                ),
                usage=UsageStats(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0,
                    latency_seconds=elapsed,
                    model_name=self._model_id,
                ),
            )
        finally:
            timer.cancel()

        elapsed = time.perf_counter() - start

        token_usage = run_result.token_usage
        prompt_tokens = token_usage.input_tokens if token_usage else 0
        completion_tokens = token_usage.output_tokens if token_usage else 0
        total_tokens = token_usage.total_tokens if token_usage else (
            prompt_tokens + completion_tokens
        )

        trace = self._runtime.tool_trace()
        return RunResult(
            answer=Answer(
                question_id="",
                text=str(run_result.output or ""),
                sources_used=self._runtime.sources_used(),
                metadata={
                    "mode": self._mode,
                    "prompt_version": PROMPT_VERSION,
                    "prompt_hash": get_system_prompt_hash(),
                    "agent_state": str(run_result.state),
                    "planning_interval": self._planning_interval,
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
                model_name=self._model_id,
            ),
        )

    async def cleanup(self) -> None:
        """Release runtime resources."""
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
