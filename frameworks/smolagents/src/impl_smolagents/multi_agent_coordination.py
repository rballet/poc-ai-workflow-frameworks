"""smolagents implementation for the multi_agent_coordination scenario.

Uses native smolagents Tool subclass pattern: specialist agents are wrapped as
Tool subclasses whose forward() creates a ToolCallingAgent with domain-specific
tools. The coordinator is a ToolCallingAgent with specialist tools.
"""

from __future__ import annotations

import asyncio
import time
from functools import partial
from typing import Any

from smolagents import LiteLLMModel, Tool, ToolCallingAgent

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.multi_agent_coordination import (
    PROMPT_VERSION,
    MultiAgentRuntime,
    build_task_prompt,
    get_coordinator_prompt,
    get_coordinator_prompt_hash,
    get_specialist_prompt,
)
from shared.retrieval import EmbeddingStore

MODEL_ID = "openai/gpt-5-mini"
TOP_K = 4


# --- Domain-specific tools (used by specialist agents) ---


class InfraSQLTool(Tool):
    """Execute read-only SQL on infrastructure tables."""

    name = "query_infrastructure"
    description = (
        "Execute read-only SQL (SELECT/WITH/PRAGMA) on infrastructure tables: "
        "clusters, services, dependencies, recent_deploys, incidents, incident_timeline."
    )
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
    description = (
        "Execute read-only SQL (SELECT/WITH/PRAGMA) on security tables: "
        "vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline."
    )
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
    description = "Search operational runbooks and policy documents for relevant evidence."
    inputs = {"query": {"type": "string", "description": "Search query"}}
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime) -> None:
        super().__init__()
        self._runtime = runtime

    def forward(self, query: str) -> str:
        return self._runtime.lookup_runbook(query)


# --- Specialist agent wrappers (used as tools by the coordinator) ---


class InfrastructureSpecialist(Tool):
    """Consult the infrastructure specialist for server, cluster, deploy, and dependency information."""

    name = "consult_infrastructure"
    description = (
        "Consult the infrastructure specialist. Ask questions about servers, "
        "clusters, deployments, service dependencies, and infrastructure state."
    )
    inputs = {
        "question": {"type": "string", "description": "Question for the infrastructure expert"},
    }
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime, model_id: str) -> None:
        super().__init__()
        self._runtime = runtime
        self._model_id = model_id

    def forward(self, question: str) -> str:
        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)
        agent = ToolCallingAgent(
            tools=[InfraSQLTool(self._runtime)],
            model=model,
            instructions=get_specialist_prompt("infrastructure"),
            max_steps=3,
            verbosity_level=0,
        )
        result = agent.run(question, max_steps=3)
        return str(result)


class SecuritySpecialist(Tool):
    """Consult the security specialist for vulnerability, access log, and firewall information."""

    name = "consult_security"
    description = (
        "Consult the security specialist. Ask questions about vulnerabilities, "
        "access logs, firewall rules, and security compliance."
    )
    inputs = {
        "question": {"type": "string", "description": "Question for the security expert"},
    }
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime, model_id: str) -> None:
        super().__init__()
        self._runtime = runtime
        self._model_id = model_id

    def forward(self, question: str) -> str:
        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)
        agent = ToolCallingAgent(
            tools=[SecuritySQLTool(self._runtime)],
            model=model,
            instructions=get_specialist_prompt("security"),
            max_steps=3,
            verbosity_level=0,
        )
        result = agent.run(question, max_steps=3)
        return str(result)


class RunbookSpecialist(Tool):
    """Consult the runbook specialist for policy, procedure, and compliance information."""

    name = "consult_runbook"
    description = (
        "Consult the runbook specialist. Ask questions about change management policies, "
        "incident response procedures, SLAs, and compliance rules."
    )
    inputs = {
        "question": {"type": "string", "description": "Question for the runbook expert"},
    }
    output_type = "string"

    def __init__(self, runtime: MultiAgentRuntime, model_id: str) -> None:
        super().__init__()
        self._runtime = runtime
        self._model_id = model_id

    def forward(self, question: str) -> str:
        model_kwargs: dict[str, Any] = {"model_id": self._model_id}
        if "gpt-5" not in self._model_id:
            model_kwargs["temperature"] = 0
        model = LiteLLMModel(**model_kwargs)
        agent = ToolCallingAgent(
            tools=[RunbookSearchTool(self._runtime)],
            model=model,
            instructions=get_specialist_prompt("runbook"),
            max_steps=3,
            verbosity_level=0,
        )
        result = agent.run(question, max_steps=3)
        return str(result)


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

        # Choose tools based on mode
        if self._mode == "capability":
            tools: list[Tool] = [
                InfrastructureSpecialist(self._runtime, self._model_id),
                SecuritySpecialist(self._runtime, self._model_id),
                RunbookSpecialist(self._runtime, self._model_id),
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

        start = time.perf_counter()
        run_result = await asyncio.to_thread(
            partial(
                agent.run,
                task,
                max_steps=self._max_steps,
                return_full_result=True,
            )
        )
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
