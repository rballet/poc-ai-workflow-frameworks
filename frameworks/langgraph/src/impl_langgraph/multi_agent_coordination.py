"""LangGraph implementation for the multi_agent_coordination scenario.

Uses native LangGraph multi-agent pattern: a supervisor/router node directs
queries to specialist agent nodes (infrastructure, security, runbook), each
with their own tool. A synthesizer node combines evidence into a final answer.
"""

from __future__ import annotations

import time
from typing import Any, Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

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

MODEL = "gpt-5-mini"
TOP_K = 4


def _make_llm(model: str) -> BaseChatModel:
    """Create the appropriate LangChain chat model based on model name."""
    kwargs: dict[str, Any] = {"model": model}
    if "gpt-5" not in model:
        kwargs["temperature"] = 0
    if model.startswith("claude"):
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(**kwargs)
    return ChatOpenAI(**kwargs)


ROUTER_PROMPT = (
    "You are a routing coordinator for incident response.\n"
    "Based on the conversation so far, decide which specialist to consult next:\n"
    "- 'infrastructure' for servers, clusters, deploys, service dependencies\n"
    "- 'security' for vulnerabilities, access logs, firewall rules\n"
    "- 'runbook' for policies, procedures, compliance rules\n"
    "- 'synthesize' when you have enough evidence to answer the question\n\n"
    "Respond with ONLY one of: infrastructure, security, runbook, synthesize"
)


class LangGraphRAG:
    """RAGFramework implementation using native LangGraph multi-agent coordination."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._graph = None
        self._runtime: MultiAgentRuntime | None = None

        self._mode = "baseline"
        self._scenario_name = "multi_agent_coordination"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 3

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
        default_steps = 1 if mode == "baseline" else 15
        self._max_steps = int(mode_config.get("max_steps", default_steps))
        default_calls = 3 if mode == "baseline" else 15
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_calls))

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

    def _build_baseline_graph(self):
        """Single-agent graph with all three tools (baseline mode)."""
        runtime = self._runtime
        llm = _make_llm(self._model)

        @tool("query_infrastructure")
        def query_infrastructure(query: str) -> str:
            """Execute read-only SQL (SELECT/WITH/PRAGMA) on infrastructure tables: clusters, services, dependencies, recent_deploys, incidents, incident_timeline."""
            return runtime.query_infrastructure(query)

        @tool("query_security")
        def query_security(query: str) -> str:
            """Execute read-only SQL (SELECT/WITH/PRAGMA) on security tables: vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline."""
            return runtime.query_security(query)

        @tool("lookup_runbook")
        def lookup_runbook(query: str) -> str:
            """Search operational runbooks and policy documents for relevant evidence."""
            return runtime.lookup_runbook(query)

        all_tools = [query_infrastructure, query_security, lookup_runbook]
        llm_with_tools = llm.bind_tools(all_tools)
        tool_node = ToolNode(all_tools)

        async def agent_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await llm_with_tools.ainvoke(
                [SystemMessage(content=get_coordinator_prompt()), *state["messages"]]
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

    def _build_capability_graph(self):
        """Multi-agent graph: router → specialist agents → synthesizer (capability mode)."""
        runtime = self._runtime
        llm = _make_llm(self._model)

        # --- Specialist tools ---
        @tool("query_infrastructure")
        def query_infrastructure(query: str) -> str:
            """Execute read-only SQL (SELECT/WITH/PRAGMA) on infrastructure tables: clusters, services, dependencies, recent_deploys, incidents, incident_timeline."""
            return runtime.query_infrastructure(query)

        @tool("query_security")
        def query_security(query: str) -> str:
            """Execute read-only SQL (SELECT/WITH/PRAGMA) on security tables: vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline."""
            return runtime.query_security(query)

        @tool("lookup_runbook")
        def lookup_runbook(query: str) -> str:
            """Search operational runbooks and policy documents for relevant evidence."""
            return runtime.lookup_runbook(query)

        # --- Specialist agent nodes (each with one tool) ---
        infra_llm = llm.bind_tools([query_infrastructure])
        infra_tool_node = ToolNode([query_infrastructure])

        security_llm = llm.bind_tools([query_security])
        security_tool_node = ToolNode([query_security])

        runbook_llm = llm.bind_tools([lookup_runbook])
        runbook_tool_node = ToolNode([lookup_runbook])

        async def infra_agent(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await infra_llm.ainvoke(
                [SystemMessage(content=get_specialist_prompt("infrastructure")), *state["messages"]]
            )
            return {"messages": [response]}

        async def security_agent(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await security_llm.ainvoke(
                [SystemMessage(content=get_specialist_prompt("security")), *state["messages"]]
            )
            return {"messages": [response]}

        async def runbook_agent(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await runbook_llm.ainvoke(
                [SystemMessage(content=get_specialist_prompt("runbook")), *state["messages"]]
            )
            return {"messages": [response]}

        # --- Router node ---
        async def router(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await llm.ainvoke(
                [SystemMessage(content=ROUTER_PROMPT), *state["messages"]]
            )
            return {"messages": [response]}

        def route_decision(
            state: MessagesState,
        ) -> Literal["infra_agent", "security_agent", "runbook_agent", "synthesizer"]:
            last = state["messages"][-1]
            content = ""
            if isinstance(last, AIMessage):
                content = last.content if isinstance(last.content, str) else ""
            content_lower = content.strip().lower()
            if "infrastructure" in content_lower:
                return "infra_agent"
            if "security" in content_lower:
                return "security_agent"
            if "runbook" in content_lower:
                return "runbook_agent"
            return "synthesizer"

        # --- Synthesizer node ---
        async def synthesizer(state: MessagesState) -> dict[str, list[BaseMessage]]:
            response = await llm.ainvoke(
                [
                    SystemMessage(
                        content=(
                            "You are a senior incident response coordinator. "
                            "Synthesize all the specialist findings from the conversation "
                            "into a comprehensive, evidence-grounded answer. "
                            "Cite specific data points and policy references."
                        )
                    ),
                    *state["messages"],
                ]
            )
            return {"messages": [response]}

        # --- Graph assembly ---
        workflow = StateGraph(MessagesState)

        # Nodes
        workflow.add_node("router", router)
        workflow.add_node("infra_agent", infra_agent)
        workflow.add_node("infra_tools", infra_tool_node)
        workflow.add_node("security_agent", security_agent)
        workflow.add_node("security_tools", security_tool_node)
        workflow.add_node("runbook_agent", runbook_agent)
        workflow.add_node("runbook_tools", runbook_tool_node)
        workflow.add_node("synthesizer", synthesizer)

        # Entry
        workflow.add_edge(START, "router")

        # Router → specialists or synthesizer
        workflow.add_conditional_edges(
            "router",
            route_decision,
            {
                "infra_agent": "infra_agent",
                "security_agent": "security_agent",
                "runbook_agent": "runbook_agent",
                "synthesizer": "synthesizer",
            },
        )

        # Each specialist: agent → tool_condition → tools → agent, then back to router
        workflow.add_conditional_edges(
            "infra_agent",
            tools_condition,
            path_map={"tools": "infra_tools", "__end__": "router"},
        )
        workflow.add_edge("infra_tools", "infra_agent")

        workflow.add_conditional_edges(
            "security_agent",
            tools_condition,
            path_map={"tools": "security_tools", "__end__": "router"},
        )
        workflow.add_edge("security_tools", "security_agent")

        workflow.add_conditional_edges(
            "runbook_agent",
            tools_condition,
            path_map={"tools": "runbook_tools", "__end__": "router"},
        )
        workflow.add_edge("runbook_tools", "runbook_agent")

        # Synthesizer → END
        workflow.add_edge("synthesizer", END)

        return workflow.compile()

    async def ingest(self, documents: list[Document]) -> None:
        self._runtime = MultiAgentRuntime(
            scenario_name=self._scenario_name,
            database_seed_file=self._database_seed_file,
            embedding_store=self._embedding_store,
            top_k=self._top_k,
            max_context_chunks=self._max_context_chunks,
        )
        self._runtime.prepare(documents)

        if self._mode == "capability":
            self._graph = self._build_capability_graph()
        else:
            self._graph = self._build_baseline_graph()

    async def query(self, question: str) -> RunResult:
        if self._graph is None or self._runtime is None:
            raise RuntimeError("Must call ingest() before query()")

        self._runtime.start_run(max_tool_calls=self._max_tool_calls)
        prompt = build_task_prompt(question, self._max_tool_calls)

        start = time.perf_counter()
        result = await self._graph.ainvoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={"recursion_limit": max(10, self._max_steps * 4)},
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
                total_tokens=prompt_tokens + completion_tokens,
                latency_seconds=elapsed,
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        if self._runtime is not None:
            self._runtime.cleanup()
        self._runtime = None
        self._graph = None
