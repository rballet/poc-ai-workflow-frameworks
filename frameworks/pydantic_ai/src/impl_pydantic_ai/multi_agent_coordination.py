"""Pydantic AI implementation for the multi_agent_coordination scenario.

Uses native Pydantic AI agent-as-tool pattern: a coordinator Agent has three
tool functions that internally invoke specialist Agent instances, each with
their own domain-specific tool.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from pydantic_ai import Agent, RunContext

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

MODEL = "openai:gpt-5-mini"
TOP_K = 4


@dataclass
class CoordinationDeps:
    """Dependencies shared across coordinator and specialist agents."""

    runtime: MultiAgentRuntime
    infra_agent: Agent | None = None
    security_agent: Agent | None = None
    runbook_agent: Agent | None = None
    # Accumulate tokens from sub-agent runs
    sub_prompt_tokens: int = field(default=0, init=False)
    sub_completion_tokens: int = field(default=0, init=False)


@dataclass(frozen=True)
class SpecialistDeps:
    """Dependencies for a specialist agent."""

    runtime: MultiAgentRuntime


class PydanticAIRAG:
    """RAGFramework implementation using native Pydantic AI multi-agent coordination."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._coordinator: Agent[CoordinationDeps, str] | None = None
        self._runtime: MultiAgentRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "multi_agent_coordination"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_tool_calls = 3

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
        default_calls = 3 if mode == "baseline" else 15
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_calls))

        if self._runtime is not None:
            self._runtime.set_limits(
                top_k=self._top_k,
                max_context_chunks=self._max_context_chunks,
            )

    def _build_specialist_agents(self) -> tuple[Agent, Agent, Agent]:
        """Create three specialist agents, each with one domain tool."""

        # --- Infrastructure specialist ---
        async def infra_query(ctx: RunContext[SpecialistDeps], query: str) -> str:
            """Execute read-only SQL on infrastructure tables."""
            return ctx.deps.runtime.query_infrastructure(query)

        infra_agent = Agent(
            self._model,
            output_type=str,
            instructions=get_specialist_prompt("infrastructure"),
            deps_type=SpecialistDeps,
            tools=[infra_query],
        )

        # --- Security specialist ---
        async def security_query(ctx: RunContext[SpecialistDeps], query: str) -> str:
            """Execute read-only SQL on security tables."""
            return ctx.deps.runtime.query_security(query)

        security_agent = Agent(
            self._model,
            output_type=str,
            instructions=get_specialist_prompt("security"),
            deps_type=SpecialistDeps,
            tools=[security_query],
        )

        # --- Runbook specialist ---
        async def runbook_search(ctx: RunContext[SpecialistDeps], query: str) -> str:
            """Search operational runbooks and policy documents."""
            return ctx.deps.runtime.lookup_runbook(query)

        runbook_agent = Agent(
            self._model,
            output_type=str,
            instructions=get_specialist_prompt("runbook"),
            deps_type=SpecialistDeps,
            tools=[runbook_search],
        )

        return infra_agent, security_agent, runbook_agent

    def _build_baseline_coordinator(self) -> Agent[CoordinationDeps, str]:
        """Single agent with all three tools (baseline mode)."""

        async def query_infrastructure(
            ctx: RunContext[CoordinationDeps], query: str
        ) -> str:
            """Execute read-only SQL on infrastructure tables."""
            return ctx.deps.runtime.query_infrastructure(query)

        async def query_security(
            ctx: RunContext[CoordinationDeps], query: str
        ) -> str:
            """Execute read-only SQL on security tables."""
            return ctx.deps.runtime.query_security(query)

        async def lookup_runbook(
            ctx: RunContext[CoordinationDeps], query: str
        ) -> str:
            """Search operational runbooks and policy documents."""
            return ctx.deps.runtime.lookup_runbook(query)

        return Agent(
            self._model,
            output_type=str,
            instructions=get_coordinator_prompt(),
            deps_type=CoordinationDeps,
            tools=[query_infrastructure, query_security, lookup_runbook],
        )

    def _build_capability_coordinator(
        self,
    ) -> Agent[CoordinationDeps, str]:
        """Coordinator agent that delegates to specialist agents (capability mode)."""

        async def consult_infrastructure(
            ctx: RunContext[CoordinationDeps], question: str
        ) -> str:
            """Consult the infrastructure specialist for server, cluster, deploy, and dependency information."""
            agent = ctx.deps.infra_agent
            if agent is None:
                return ctx.deps.runtime.query_infrastructure(question)
            result = await agent.run(
                question, deps=SpecialistDeps(runtime=ctx.deps.runtime)
            )
            usage = result.usage()
            ctx.deps.sub_prompt_tokens += usage.input_tokens or 0
            ctx.deps.sub_completion_tokens += usage.output_tokens or 0
            return result.output

        async def consult_security(
            ctx: RunContext[CoordinationDeps], question: str
        ) -> str:
            """Consult the security specialist for vulnerability, access log, and firewall information."""
            agent = ctx.deps.security_agent
            if agent is None:
                return ctx.deps.runtime.query_security(question)
            result = await agent.run(
                question, deps=SpecialistDeps(runtime=ctx.deps.runtime)
            )
            usage = result.usage()
            ctx.deps.sub_prompt_tokens += usage.input_tokens or 0
            ctx.deps.sub_completion_tokens += usage.output_tokens or 0
            return result.output

        async def consult_runbook(
            ctx: RunContext[CoordinationDeps], question: str
        ) -> str:
            """Consult the runbook specialist for policy, procedure, and compliance information."""
            agent = ctx.deps.runbook_agent
            if agent is None:
                return ctx.deps.runtime.lookup_runbook(question)
            result = await agent.run(
                question, deps=SpecialistDeps(runtime=ctx.deps.runtime)
            )
            usage = result.usage()
            ctx.deps.sub_prompt_tokens += usage.input_tokens or 0
            ctx.deps.sub_completion_tokens += usage.output_tokens or 0
            return result.output

        return Agent(
            self._model,
            output_type=str,
            instructions=get_coordinator_prompt(),
            deps_type=CoordinationDeps,
            tools=[consult_infrastructure, consult_security, consult_runbook],
        )

    def _ensure_coordinator(self) -> Agent[CoordinationDeps, str]:
        if self._coordinator is not None:
            return self._coordinator

        if self._mode == "capability":
            self._coordinator = self._build_capability_coordinator()
        else:
            self._coordinator = self._build_baseline_coordinator()
        return self._coordinator

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

        coordinator = self._ensure_coordinator()
        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        # Build deps with specialist agents for capability mode
        infra_agent = security_agent = runbook_agent = None
        if self._mode == "capability":
            infra_agent, security_agent, runbook_agent = (
                self._build_specialist_agents()
            )

        deps = CoordinationDeps(
            runtime=self._runtime,
            infra_agent=infra_agent,
            security_agent=security_agent,
            runbook_agent=runbook_agent,
        )

        prompt = build_task_prompt(question, self._max_tool_calls)

        start = time.perf_counter()
        result = await coordinator.run(prompt, deps=deps)
        elapsed = time.perf_counter() - start

        usage = result.usage()
        prompt_tokens = (usage.input_tokens or 0) + deps.sub_prompt_tokens
        completion_tokens = (usage.output_tokens or 0) + deps.sub_completion_tokens
        total_tokens = usage.total_tokens or (prompt_tokens + completion_tokens)
        # Add sub-agent tokens to total if not already counted
        if deps.sub_prompt_tokens or deps.sub_completion_tokens:
            total_tokens = prompt_tokens + completion_tokens

        trace = self._runtime.tool_trace()
        return RunResult(
            answer=Answer(
                question_id="",
                text=result.output,
                sources_used=self._runtime.sources_used(),
                metadata={
                    "mode": self._mode,
                    "prompt_version": PROMPT_VERSION,
                    "prompt_hash": get_coordinator_prompt_hash(),
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
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
        self._coordinator = None
