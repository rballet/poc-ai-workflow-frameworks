"""LangGraph implementation for the agentic_sql_qa scenario."""

from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from shared.agentic_sql import (
    PROMPT_VERSION,
    AgenticSQLRuntime,
    get_system_prompt,
    get_system_prompt_hash,
)
from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore

MODEL = "gpt-5-mini"
TOP_K = 4


class LangGraphRAG:
    """RAGFramework implementation using native LangGraph tool-calling."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._graph = None
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
        return "LangGraph"

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
        default_tool_calls = 1 if mode == "baseline" else 8
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_tool_calls))

        if self._runtime is not None:
            self._runtime.set_limits(
                top_k=self._top_k,
                max_context_chunks=self._max_context_chunks,
            )

    @staticmethod
    def _sum_usage(messages: list[BaseMessage]) -> tuple[int, int]:
        prompt_tokens = 0
        completion_tokens = 0
        for message in messages:
            if not isinstance(message, AIMessage):
                continue
            usage = message.usage_metadata or {}
            prompt_tokens += int(usage.get("input_tokens", 0))
            completion_tokens += int(usage.get("output_tokens", 0))
        return prompt_tokens, completion_tokens

    @staticmethod
    def _ai_text(messages: list[BaseMessage]) -> str:
        for message in reversed(messages):
            if isinstance(message, AIMessage):
                content = message.content
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    parts: list[str] = []
                    for item in content:
                        if isinstance(item, str):
                            parts.append(item)
                        elif isinstance(item, dict):
                            text = item.get("text")
                            if isinstance(text, str):
                                parts.append(text)
                    if parts:
                        return "\n".join(parts)
        return ""

    def _build_graph(self):
        """Build native LangGraph tool-calling loop."""
        runtime = self._runtime
        llm_kwargs: dict = {"model": self._model}
        if "gpt-5" not in self._model:
            llm_kwargs["temperature"] = 0
        llm = ChatOpenAI(**llm_kwargs)

        @tool("run_sql")
        def run_sql(query: str) -> str:
            """Execute read-only SQL (SELECT/WITH/PRAGMA) against the scenario SQLite database."""
            return runtime.run_sql(query)

        @tool("lookup_doc")
        def lookup_doc(query: str) -> str:
            """Search scenario policy/process documents for relevant evidence."""
            return runtime.lookup_doc(query)

        llm_with_tools = llm.bind_tools([run_sql, lookup_doc])
        tool_node = ToolNode([run_sql, lookup_doc])

        async def agent_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await llm_with_tools.ainvoke(
                [SystemMessage(content=get_system_prompt()), *state["messages"]]
            )
            return {"messages": [response]}

        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            path_map={"tools": "tools", "__end__": END},
        )
        workflow.add_edge("tools", "agent")
        return workflow.compile()

    async def ingest(self, documents: list[Document]) -> None:
        """Prepare shared runtime and tool-calling graph."""
        self._runtime = AgenticSQLRuntime(
            scenario_name=self._scenario_name,
            database_seed_file=self._database_seed_file,
            embedding_store=self._embedding_store,
            top_k=self._top_k,
            max_context_chunks=self._max_context_chunks,
        )
        self._runtime.prepare(documents)
        self._graph = self._build_graph()

    async def query(self, question: str) -> RunResult:
        """Answer question through native LangGraph tool-calling."""
        if self._graph is None or self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        self._runtime.start_run(max_tool_calls=self._max_tool_calls)

        start = time.perf_counter()
        result = await self._graph.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            config={"recursion_limit": max(8, self._max_steps * 4)},
        )
        elapsed = time.perf_counter() - start

        messages: list[BaseMessage] = result.get("messages", [])
        prompt_tokens, completion_tokens = self._sum_usage(messages)
        answer_text = self._ai_text(messages)
        trace = self._runtime.tool_trace()

        return RunResult(
            answer=Answer(
                question_id="",
                text=answer_text,
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
                total_tokens=prompt_tokens + completion_tokens,
                latency_seconds=elapsed,
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        """Release runtime resources."""
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
        self._graph = None
