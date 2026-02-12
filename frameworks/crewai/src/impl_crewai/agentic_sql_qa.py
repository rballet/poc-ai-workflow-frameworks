"""CrewAI implementation for the agentic_sql_qa scenario.

Uses CrewAI's native tool-calling with Agent/Task/Crew. Tools delegate to
the shared AgenticSQLRuntime for run_sql and lookup_doc operations.
"""

from __future__ import annotations

import time
from typing import Any, Type

from crewai import Agent, Crew, LLM, Task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

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

MODEL = "openai/gpt-5-mini"
TOP_K = 4


class SQLInput(BaseModel):
    query: str = Field(description="SQL query to execute")


class DocInput(BaseModel):
    query: str = Field(description="Search query for policy/process documents")


class RunSQLTool(BaseTool):
    """Execute read-only SQL on the scenario SQLite database."""

    name: str = "run_sql"
    description: str = RUN_SQL_DESC
    args_schema: Type[BaseModel] = SQLInput
    runtime: AgenticSQLRuntime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, query: str, **kwargs: Any) -> str:
        if self.runtime is None:
            return "Error: runtime not initialized"
        return self.runtime.run_sql(query)


class LookupDocTool(BaseTool):
    """Search scenario policy/process documents."""

    name: str = "lookup_doc"
    description: str = LOOKUP_DOC_DESC
    args_schema: Type[BaseModel] = DocInput
    runtime: AgenticSQLRuntime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _run(self, query: str, **kwargs: Any) -> str:
        if self.runtime is None:
            return "Error: runtime not initialized"
        return self.runtime.lookup_doc(query)


class CrewAIRAG:
    """RAGFramework implementation using CrewAI native tool-calling."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._runtime: AgenticSQLRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "agentic_sql_qa"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 1

    @property
    def name(self) -> str:
        return "CrewAI"

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
        """Answer question through CrewAI's native tool-calling loop."""
        if self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        sql_tool = RunSQLTool(runtime=self._runtime)
        doc_tool = LookupDocTool(runtime=self._runtime)

        llm = LLM(model=self._model)
        agent = Agent(
            role="SQL & Policy Analyst",
            goal="Answer questions using SQL queries and policy document lookups",
            backstory=get_system_prompt(),
            llm=llm,
            tools=[sql_tool, doc_tool],
            verbose=False,
            max_iter=self._max_steps + 2,
        )

        prompt = build_task_prompt(question, self._max_tool_calls)
        task = Task(
            description=prompt,
            expected_output="A grounded answer based on SQL results and/or policy documents.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=False)

        start = time.perf_counter()
        result = await crew.kickoff_async()
        elapsed = time.perf_counter() - start

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
