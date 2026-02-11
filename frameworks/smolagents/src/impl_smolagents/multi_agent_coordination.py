"""smolagents implementation for the multi_agent_coordination scenario.

Uses native smolagents Tool subclass pattern: specialist agents are wrapped as
Tool subclasses whose forward() creates a ToolCallingAgent with domain-specific
tools. The coordinator is a ToolCallingAgent with specialist tools.
"""

from __future__ import annotations

import asyncio
import threading
import time
from functools import partial
from typing import Any

from smolagents import LiteLLMModel, Tool, ToolCallingAgent

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.multi_agent_coordination import (
    CONSULT_INFRASTRUCTURE_DESC,
    CONSULT_RUNBOOK_DESC,
    CONSULT_SECURITY_DESC,
    LOOKUP_RUNBOOK_DESC,
    PROMPT_VERSION,
    QUERY_INFRASTRUCTURE_DESC,
    QUERY_SECURITY_DESC,
    MultiAgentRuntime,
    build_task_prompt,
    get_coordinator_prompt,
    get_coordinator_prompt_hash,
    get_specialist_prompt,
)
from shared.retrieval import EmbeddingStore

MODEL_ID = "openai/gpt-5-mini"
TOP_K = 4
# smolagents injects ~700+ tokens of internal prompting per agent step, and
# gpt-5-mini does not support the `stop` parameter used by smolagents to
# interrupt generation.  Sub-agents therefore need more steps than other
# frameworks to produce a tool-call + final answer cycle.
SUB_AGENT_MAX_STEPS = 6


# --- Domain-specific tools (used by specialist agents) ---


class InfraSQLTool(Tool):
    """Execute read-only SQL on infrastructure tables."""

    name = "query_infrastructure"
    description = QUERY_INFRASTRUCTURE_DESC
    inputs = {"query": {"type": "string", "description": "SQL query to execute"}}
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.query_infrastructure(query)


class SecuritySQLTool(Tool):
    """Execute read-only SQL on security tables."""

    name = "query_security"
    description = QUERY_SECURITY_DESC
    inputs = {"query": {"type": "string", "description": "SQL query to execute"}}
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.query_security(query)


class RunbookSearchTool(Tool):
    """Search operational runbooks and policy documents."""

    name = "lookup_runbook"
    description = LOOKUP_RUNBOOK_DESC
    inputs = {"query": {"type": "string", "description": "Search query"}}
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.lookup_runbook(query)


# --- Specialist agent wrappers (used as tools by the coordinator) ---


class _SpecialistBase(Tool):
    """Base class for specialist agent tools with shared timeout support.

    Each specialist creates a ToolCallingAgent in forward().  A shared
    ``threading.Event`` (``_cancel``) is checked before starting the sub-agent;
    the coordinator sets the event when the global timeout fires so that
    remaining specialist calls return immediately instead of burning API quota.
    """

    output_type = "string"

    def __init__(
        self,
        runtime: MultiAgentRuntime,
        model_id: str,
        cancel: threading.Event | None = None,
    ) -> None:
        super().__init__()
        self._runtime = runtime
        self._model_id = model_id
        self._cancel = cancel or threading.Event()

    def _run_specialist(
        self,
        question: str,
        tool: Tool,
        domain: str,
    ) -> str:
        if self._cancel.is_set():
            return f"{domain} specialist skipped (timeout)."
        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)
        agent = ToolCallingAgent(
            tools=[tool],
            model=model,
            instructions=get_specialist_prompt(domain),
            max_steps=SUB_AGENT_MAX_STEPS,
            verbosity_level=0,
        )
        result = agent.run(
            question,
            max_steps=SUB_AGENT_MAX_STEPS,
            return_full_result=True,
        )
        return str(result.output or f"No answer produced by {domain} specialist.")


class InfrastructureSpecialist(_SpecialistBase):
    """Consult the infrastructure specialist for server, cluster, deploy, and dependency information."""

    name = "consult_infrastructure"
    description = CONSULT_INFRASTRUCTURE_DESC
    inputs = {
        "question": {"type": "string", "description": "Question for the infrastructure expert"},
    }

    def forward(self, question: str) -> str:
        return self._run_specialist(question, InfraSQLTool(self._runtime), "infrastructure")


class SecuritySpecialist(_SpecialistBase):
    """Consult the security specialist for vulnerability, access log, and firewall information."""

    name = "consult_security"
    description = CONSULT_SECURITY_DESC
    inputs = {
        "question": {"type": "string", "description": "Question for the security expert"},
    }

    def forward(self, question: str) -> str:
        return self._run_specialist(question, SecuritySQLTool(self._runtime), "security")


class RunbookSpecialist(_SpecialistBase):
    """Consult the runbook specialist for policy, procedure, and compliance information."""

    name = "consult_runbook"
    description = CONSULT_RUNBOOK_DESC
    inputs = {
        "question": {"type": "string", "description": "Question for the runbook expert"},
    }

    def forward(self, question: str) -> str:
        return self._run_specialist(question, RunbookSearchTool(self._runtime), "runbook")


class SmolAgentsRAG:
    """RAGFramework implementation using native smolagents multi-agent coordination."""

    def __init__(
        self,
        model_id: str = MODEL_ID,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model_id = model_id
        self._embedding_store = embedding_store
        self._runtime: MultiAgentRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "multi_agent_coordination"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 3
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
        _ = scenario_type
        self._mode = mode
        self._scenario_name = scenario_name
        self._database_seed_file = str(
            scenario_config.get("database_seed_file", "data/seed.sql")
        )
        self._top_k = int(
            mode_config.get("top_k", scenario_config.get("top_k", TOP_K))
        )
        self._max_context_chunks = int(
            mode_config.get("max_context_chunks", self._top_k)
        )
        default_steps = 1 if mode == "baseline" else 8
        self._max_steps = int(mode_config.get("max_steps", default_steps))
        default_calls = 3 if mode == "baseline" else 15
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_calls))
        default_planning: int | None = None if mode == "baseline" else 1
        planning = mode_config.get("planning_interval", default_planning)
        self._planning_interval = None if planning is None else int(planning)

        if self._runtime is not None:
            self._runtime.set_limits(
                top_k=self._top_k,
                max_context_chunks=self._max_context_chunks,
            )

    async def ingest(self, documents: list[Document]) -> None:
        self._runtime = MultiAgentRuntime(
            scenario_name=self._scenario_name,
            database_seed_file=self._database_seed_file,
            embedding_store=self._embedding_store,
            top_k=self._top_k,
            max_context_chunks=self._max_context_chunks,
        )
        self._runtime.prepare(documents)

    async def query(self, question: str) -> RunResult:
        if self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)

        # Shared cancel event — set by the timeout timer so that both the
        # coordinator and any in-flight specialist sub-agents stop promptly.
        cancel = threading.Event()

        # Choose tools based on mode
        if self._mode == "capability":
            tools: list[Tool] = [
                InfrastructureSpecialist(self._runtime, self._model_id, cancel),
                SecuritySpecialist(self._runtime, self._model_id, cancel),
                RunbookSpecialist(self._runtime, self._model_id, cancel),
            ]
        else:
            tools = [
                InfraSQLTool(self._runtime),
                SecuritySQLTool(self._runtime),
                RunbookSearchTool(self._runtime),
            ]

        agent = ToolCallingAgent(
            tools=tools,
            model=model,
            instructions=get_coordinator_prompt(),
            planning_interval=self._planning_interval,
            max_steps=self._max_steps,
            verbosity_level=0,
        )

        task = build_task_prompt(question, self._max_tool_calls)

        # Use a timer to interrupt the agent if it exceeds the timeout.
        # asyncio.wait_for() cannot cancel threads spawned by to_thread(),
        # so we use smolagents' native interrupt_switch mechanism *and* set
        # the cancel event so that specialist sub-agents bail out early.
        timeout_seconds = 120.0

        def _on_timeout() -> None:
            cancel.set()
            agent.interrupt()

        timer = threading.Timer(timeout_seconds, _on_timeout)
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
            # Agent was interrupted or errored — produce a fallback result
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
                        "prompt_hash": get_coordinator_prompt_hash(),
                        "agent_state": "interrupted",
                        "planning_interval": self._planning_interval,
                        "tool_trace": trace,
                        "tool_calls": self._runtime.tool_calls(),
                        "agents_used": self._runtime.agents_used(),
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
        total_tokens = (
            token_usage.total_tokens
            if token_usage
            else (prompt_tokens + completion_tokens)
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
                    "prompt_hash": get_coordinator_prompt_hash(),
                    "agent_state": str(run_result.state),
                    "planning_interval": self._planning_interval,
                    "tool_trace": trace,
                    "tool_calls": self._runtime.tool_calls(),
                    "agents_used": self._runtime.agents_used(),
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
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
