"""CrewAI implementation for the multi_agent_coordination scenario.

Baseline: single agent with all 3 domain tools (direct access).
Capability: hierarchical Crew with a coordinator manager and three specialist
agents, each with their domain-specific tool. CrewAI's Process.hierarchical
handles delegation automatically.
"""

from __future__ import annotations

import time
from typing import Any, Type

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.multi_agent_coordination import (
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

MODEL = "openai/gpt-5-mini"
TOP_K = 4


# --- Input schemas ---

class QueryInput(BaseModel):
    query: str = Field(description="SQL query to execute")


class SearchInput(BaseModel):
    query: str = Field(description="Search query for documents")


# --- Domain tools ---

class QueryInfrastructureTool(BaseTool):
    name: str = "query_infrastructure"
    description: str = QUERY_INFRASTRUCTURE_DESC
    args_schema: Type[BaseModel] = QueryInput
    runtime: MultiAgentRuntime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, query: str, **kwargs: Any) -> str:
        if self.runtime is None:
            return "Error: runtime not initialized"
        return self.runtime.query_infrastructure(query)


class QuerySecurityTool(BaseTool):
    name: str = "query_security"
    description: str = QUERY_SECURITY_DESC
    args_schema: Type[BaseModel] = QueryInput
    runtime: MultiAgentRuntime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, query: str, **kwargs: Any) -> str:
        if self.runtime is None:
            return "Error: runtime not initialized"
        return self.runtime.query_security(query)


class LookupRunbookTool(BaseTool):
    name: str = "lookup_runbook"
    description: str = LOOKUP_RUNBOOK_DESC
    args_schema: Type[BaseModel] = SearchInput
    runtime: MultiAgentRuntime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, query: str, **kwargs: Any) -> str:
        if self.runtime is None:
            return "Error: runtime not initialized"
        return self.runtime.lookup_runbook(query)


class CrewAIRAG:
    """RAGFramework implementation using CrewAI multi-agent coordination."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._runtime: MultiAgentRuntime | None = None
        self._llm: LLM | None = None

        self._mode = "baseline"
        self._scenario_name = "multi_agent_coordination"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 3

    @property
    def name(self) -> str:
        return "CrewAI"

    def _ensure_llm(self) -> LLM:
        if self._llm is None:
            self._llm = LLM(model=self._model)
        return self._llm

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
        llm = self._ensure_llm()

        prompt = build_task_prompt(question, self._max_tool_calls)

        if self._mode == "capability":
            result, elapsed = await self._query_capability(llm, prompt)
        else:
            result, elapsed = await self._query_baseline(llm, prompt)

        tu = result.token_usage
        prompt_tokens = tu.prompt_tokens if tu else 0
        completion_tokens = tu.completion_tokens if tu else 0
        total_tokens = tu.total_tokens if tu else (prompt_tokens + completion_tokens)

        trace = self._runtime.tool_trace()
        return RunResult(
            answer=Answer(
                question_id="",
                text=result.raw or "",
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

    async def _query_baseline(self, llm: Any, prompt: str) -> tuple:
        """Single agent with all 3 direct tools."""
        tools = [
            QueryInfrastructureTool(runtime=self._runtime),
            QuerySecurityTool(runtime=self._runtime),
            LookupRunbookTool(runtime=self._runtime),
        ]
        agent = Agent(
            role="Incident Response Coordinator",
            goal="Answer incident response questions using infrastructure, security, and runbook tools",
            backstory=get_coordinator_prompt(),
            llm=llm,
            tools=tools,
            verbose=False,
            max_iter=self._max_steps + 2,
        )
        task = Task(
            description=prompt,
            expected_output="A comprehensive answer based on tool evidence.",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task], verbose=False)

        start = time.perf_counter()
        result = await crew.kickoff_async()
        elapsed = time.perf_counter() - start
        return result, elapsed

    async def _query_capability(self, llm: Any, prompt: str) -> tuple:
        """Hierarchical Crew with coordinator + specialist agents."""
        # Specialist agents with domain-specific tools
        infra_agent = Agent(
            role="Infrastructure Specialist",
            goal="Answer infrastructure questions by querying service, cluster, and deployment data",
            backstory=get_specialist_prompt("infrastructure"),
            llm=llm,
            tools=[QueryInfrastructureTool(runtime=self._runtime)],
            verbose=False,
            max_iter=8,
        )
        security_agent = Agent(
            role="Security Specialist",
            goal="Answer security questions by querying vulnerability, firewall, and access log data",
            backstory=get_specialist_prompt("security"),
            llm=llm,
            tools=[QuerySecurityTool(runtime=self._runtime)],
            verbose=False,
            max_iter=8,
        )
        runbook_agent = Agent(
            role="Runbook Specialist",
            goal="Answer operations questions using runbook and policy documents",
            backstory=get_specialist_prompt("runbook"),
            llm=llm,
            tools=[LookupRunbookTool(runtime=self._runtime)],
            verbose=False,
            max_iter=8,
        )

        # Coordinator as manager
        coordinator = Agent(
            role="Incident Response Coordinator",
            goal="Synthesize answers from specialist agents to resolve incident response questions",
            backstory=get_coordinator_prompt(),
            llm=llm,
            verbose=False,
            max_iter=self._max_steps + 2,
            allow_delegation=True,
        )

        task = Task(
            description=prompt,
            expected_output="A comprehensive answer synthesizing information from infrastructure, security, and runbook specialists.",
        )

        crew = Crew(
            agents=[infra_agent, security_agent, runbook_agent],
            tasks=[task],
            process=Process.hierarchical,
            manager_agent=coordinator,
            verbose=False,
        )

        start = time.perf_counter()
        result = await crew.kickoff_async()
        elapsed = time.perf_counter() - start
        return result, elapsed

    async def cleanup(self) -> None:
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
