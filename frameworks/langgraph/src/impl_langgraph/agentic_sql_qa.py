"""LangGraph implementation for the agentic_sql_qa scenario."""

from __future__ import annotations

import json
import re
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any

import chromadb
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from typing_extensions import TypedDict

from shared.interface import Answer, Document, RunResult, UsageStats
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4

PLANNER_SYSTEM_PROMPT = (
    "You are orchestrating tools for a support analytics task. "
    "Available tools:\n"
    "- run_sql(query): read-only SQL against operational tables. Supports "
    "SELECT, WITH, sqlite_master table listing, and PRAGMA table_info(table) "
    "for schema introspection.\n"
    "- lookup_doc(query): retrieve policy/escalation documentation.\n\n"
    "Return strict JSON with keys: "
    '{"action":"run_sql|lookup_doc|final","input":"...","reason":"..."}.\n'
    "Never invent table or column names. Use only names observed in prior tool "
    "outputs. If schema is unknown, first query sqlite_master. If columns are "
    "unknown, run PRAGMA table_info(<table>) before business SQL.\n"
    "If run_sql returns an error like no such table/column, do not guess: "
    "inspect schema and retry with corrected names.\n"
    "For decision questions (eligibility/escalation/compensation), gather both "
    "facts (SQL) and policy evidence (lookup_doc) before finalizing.\n"
    "Choose final only when evidence is enough to answer confidently."
)

ANSWER_SYSTEM_PROMPT = (
    "You are a precise support operations assistant. "
    "Use only the gathered tool evidence. "
    "If evidence is insufficient, say exactly what is missing. "
    "Cite concrete entities or values from evidence."
)


class AgenticState(TypedDict):
    """State for plan -> tool -> plan loop."""

    question: str
    evidence: list[str]
    sources: list[str]
    sql_trace: list[str]
    doc_trace: list[str]
    tool_trace: list[dict[str, str]]
    steps: int
    tool_calls: int
    max_steps: int
    max_tool_calls: int
    next_action: str
    next_input: str
    answer: str
    input_tokens: int
    output_tokens: int


class LangGraphRAG:
    """RAGFramework implementation using LangGraph with explicit tools."""

    def __init__(
        self,
        model: str = MODEL,
        embedding_store: EmbeddingStore | None = None,
    ) -> None:
        self._model = model
        self._embedding_store = embedding_store
        self._graph = None

        # Configuration from scenario/mode.
        self._mode = "baseline"
        self._scenario_name = "agentic_sql_qa"
        self._database_seed_file = "data/seed.sql"
        self._top_k = TOP_K
        self._max_context_chunks = TOP_K
        self._max_steps = 1
        self._max_tool_calls = 1

        # SQLite state.
        self._conn: sqlite3.Connection | None = None

        # Doc retrieval state when shared embedding store is not used.
        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"langgraph_agentic_sql_{uuid.uuid4().hex[:8]}"
        else:
            self._chroma_client = None
            self._openai_client = None
            self._collection = None
            self._collection_name = None

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
        default_steps = 1 if mode == "baseline" else 6
        self._max_steps = int(mode_config.get("max_steps", default_steps))
        default_tool_calls = 1 if mode == "baseline" else 6
        self._max_tool_calls = int(mode_config.get("max_tool_calls", default_tool_calls))

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    @staticmethod
    def _merge_unique(existing: list[str], incoming: list[str]) -> list[str]:
        merged = list(existing)
        seen = set(existing)
        for item in incoming:
            if item not in seen:
                merged.append(item)
                seen.add(item)
        return merged

    @staticmethod
    def _extract_sql_sources(query: str) -> list[str]:
        tables = re.findall(
            r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
            query,
            flags=re.IGNORECASE,
        )
        deduped: list[str] = []
        seen: set[str] = set()
        for table in tables:
            lower = table.lower()
            if lower not in seen:
                seen.add(lower)
                deduped.append(lower)
        return deduped

    @staticmethod
    def _safe_json_parse(text: str) -> dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if not match:
                return {}
            try:
                return json.loads(match.group(0))
            except Exception:
                return {}

    @staticmethod
    def _usage_delta(response) -> tuple[int, int]:
        usage = response.usage_metadata or {}
        return usage.get("input_tokens", 0), usage.get("output_tokens", 0)

    def _resolve_seed_sql_path(self) -> Path:
        repo_root = Path(__file__).resolve().parents[4]
        return repo_root / "scenarios" / self._scenario_name / self._database_seed_file

    def _schema_brief(self) -> str:
        if self._conn is None:
            return "Schema unavailable (database not initialized)."
        tables = [
            str(row["name"])
            for row in self._conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        ]
        if not tables:
            return "No tables found."

        lines: list[str] = []
        for table in tables:
            rows = self._conn.execute(f"PRAGMA table_info({table})").fetchall()
            columns = [str(row["name"]) for row in rows]
            lines.append(f"{table}: {', '.join(columns)}")
        return "\n".join(lines)

    def _known_tables(self) -> set[str]:
        if self._conn is None:
            return set()
        return {
            str(row["name"]).lower()
            for row in self._conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

    @staticmethod
    def _is_safe_sql(query: str) -> bool:
        lowered = query.lower()
        if ";" in query:
            return False
        destructive = re.search(
            r"\b(insert|update|delete|drop|alter|create|replace|truncate|"
            r"attach|detach|vacuum|reindex)\b",
            lowered,
        )
        if destructive:
            return False
        return lowered.startswith("select") or lowered.startswith("with") or lowered.startswith("pragma")

    def _init_db(self) -> None:
        seed_path = self._resolve_seed_sql_path()
        if not seed_path.exists():
            raise FileNotFoundError(f"SQLite seed file not found: {seed_path}")
        if self._conn is not None:
            self._conn.close()
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(seed_path.read_text())
        self._conn.commit()

    def _retrieve_docs(self, query: str, top_k: int) -> RetrievalResult:
        if self._embedding_store is not None:
            return self._embedding_store.retrieve(query, top_k=top_k)

        openai_client = self._ensure_openai()
        response = openai_client.embeddings.create(model=EMBEDDING_MODEL, input=query)
        query_embedding = response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        chunks: list[str] = []
        sources: list[str] = []
        if results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                source = meta.get("source", "unknown")
                chunks.append(f"[Source: {source}]\n{doc}")
                if source not in sources:
                    sources.append(source)
        return RetrievalResult(chunks=chunks, sources=sources)

    def _tool_run_sql(self, query: str) -> tuple[str, list[str]]:
        if self._conn is None:
            return "Database not initialized.", []

        cleaned = query.strip().rstrip(";")
        if not cleaned:
            return "Empty SQL query.", []
        if not self._is_safe_sql(cleaned):
            hint = self._schema_brief()
            return (
                "Unsafe or unsupported SQL. Only SELECT/WITH/PRAGMA read-only "
                "queries are allowed.\n"
                f"Schema hint:\n{hint}"
            ), []

        try:
            cursor = self._conn.execute(cleaned)
            rows = [dict(row) for row in cursor.fetchall()]
            limited_rows = rows[:20]
            row_count = len(rows)
            payload = json.dumps(limited_rows, indent=2, default=str)
            tables = self._extract_sql_sources(cleaned)
            known_tables = self._known_tables()
            tables = [table for table in tables if table in known_tables]
            lowered = cleaned.lower()
            if lowered.startswith("pragma table_info("):
                match = re.search(r"pragma\s+table_info\(([^)]+)\)", lowered)
                if match:
                    tables = self._merge_unique(
                        tables,
                        [match.group(1).strip().strip("'\"")],
                    )
                    tables = [table for table in tables if table in known_tables]
            return (
                f"Row count: {row_count}\nRows (max 20):\n{payload}",
                tables,
            )
        except Exception as err:
            hint = self._schema_brief()
            return f"SQL error: {err}\nSchema hint:\n{hint}", []

    def _tool_lookup_doc(self, query: str) -> tuple[str, list[str]]:
        retrieval = self._retrieve_docs(query, top_k=self._top_k)
        chunks = retrieval.chunks[: self._max_context_chunks]
        if not chunks:
            return "No policy/document context found.", []
        return "\n\n---\n\n".join(chunks), retrieval.sources

    def _build_graph(self):
        """Build plan -> tool -> plan loop with final synthesis."""
        model = self._model

        async def plan(state: AgenticState) -> dict[str, Any]:
            if (
                state["tool_calls"] >= state["max_tool_calls"]
                or state["steps"] >= state["max_steps"]
            ):
                return {"next_action": "final", "next_input": ""}

            llm = ChatOpenAI(model=model, temperature=0)
            recent_evidence = "\n\n".join(state["evidence"][-3:]) if state["evidence"] else "None"
            user_prompt = (
                f"Question:\n{state['question']}\n\n"
                f"Mode: {self._mode}\n"
                f"Tool budget: {state['tool_calls']}/{state['max_tool_calls']}\n"
                f"Step budget: {state['steps']}/{state['max_steps']}\n"
                f"SQL trace: {state['sql_trace']}\n"
                f"Doc trace: {state['doc_trace']}\n"
                f"Recent evidence:\n{recent_evidence}"
            )
            response = await llm.ainvoke(
                [SystemMessage(content=PLANNER_SYSTEM_PROMPT), HumanMessage(content=user_prompt)]
            )
            in_t, out_t = self._usage_delta(response)
            data = self._safe_json_parse(str(response.content))
            action = str(data.get("action", "final")).strip().lower()
            tool_input = str(data.get("input", "")).strip()
            if action not in {"run_sql", "lookup_doc", "final"}:
                action = "final"
            if action != "final" and not tool_input:
                tool_input = state["question"]
            return {
                "next_action": action,
                "next_input": tool_input,
                "input_tokens": state["input_tokens"] + in_t,
                "output_tokens": state["output_tokens"] + out_t,
            }

        async def run_sql(state: AgenticState) -> dict[str, Any]:
            query = state["next_input"] or state["question"]
            observation, sources = self._tool_run_sql(query)
            evidence_entry = f"[Tool: run_sql]\nQuery:\n{query}\n\nObservation:\n{observation}"
            return {
                "evidence": state["evidence"] + [evidence_entry],
                "sources": self._merge_unique(state["sources"], sources),
                "sql_trace": state["sql_trace"] + [query],
                "tool_trace": state["tool_trace"] + [{"tool": "run_sql", "input": query}],
                "tool_calls": state["tool_calls"] + 1,
                "steps": state["steps"] + 1,
            }

        async def lookup_doc(state: AgenticState) -> dict[str, Any]:
            query = state["next_input"] or state["question"]
            observation, sources = self._tool_lookup_doc(query)
            evidence_entry = f"[Tool: lookup_doc]\nQuery:\n{query}\n\nObservation:\n{observation}"
            return {
                "evidence": state["evidence"] + [evidence_entry],
                "sources": self._merge_unique(state["sources"], sources),
                "doc_trace": state["doc_trace"] + [query],
                "tool_trace": state["tool_trace"] + [{"tool": "lookup_doc", "input": query}],
                "tool_calls": state["tool_calls"] + 1,
                "steps": state["steps"] + 1,
            }

        async def finalize(state: AgenticState) -> dict[str, Any]:
            llm = ChatOpenAI(model=model, temperature=0)
            gathered = (
                "\n\n".join(state["evidence"])
                if state["evidence"]
                else "No evidence collected."
            )
            prompt = (
                f"Question:\n{state['question']}\n\n"
                f"Evidence:\n{gathered}\n\n"
                "Provide a concise grounded answer."
            )
            response = await llm.ainvoke(
                [SystemMessage(content=ANSWER_SYSTEM_PROMPT), HumanMessage(content=prompt)]
            )
            in_t, out_t = self._usage_delta(response)
            return {
                "answer": str(response.content),
                "input_tokens": state["input_tokens"] + in_t,
                "output_tokens": state["output_tokens"] + out_t,
            }

        def route_from_plan(state: AgenticState) -> str:
            action = state.get("next_action", "final")
            if action in {"run_sql", "lookup_doc"}:
                return action
            return "final"

        workflow = StateGraph(AgenticState)
        workflow.add_node("plan", plan)
        workflow.add_node("run_sql", run_sql)
        workflow.add_node("lookup_doc", lookup_doc)
        workflow.add_node("final", finalize)
        workflow.add_edge(START, "plan")
        workflow.add_conditional_edges(
            "plan",
            route_from_plan,
            path_map={
                "run_sql": "run_sql",
                "lookup_doc": "lookup_doc",
                "final": "final",
            },
        )
        workflow.add_edge("run_sql", "plan")
        workflow.add_edge("lookup_doc", "plan")
        workflow.add_edge("final", END)
        return workflow.compile()

    async def ingest(self, documents: list[Document]) -> None:
        """Prepare SQL database and document retrieval index."""
        self._init_db()

        if self._embedding_store is not None:
            self._graph = self._build_graph()
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
        self._graph = self._build_graph()

    async def query(self, question: str) -> RunResult:
        """Answer a question through tool-driven LangGraph orchestration."""
        if self._graph is None:
            raise RuntimeError("Must call ingest() before query()")

        start = time.perf_counter()
        result = await self._graph.ainvoke(
            {
                "question": question,
                "evidence": [],
                "sources": [],
                "sql_trace": [],
                "doc_trace": [],
                "tool_trace": [],
                "steps": 0,
                "tool_calls": 0,
                "max_steps": self._max_steps,
                "max_tool_calls": self._max_tool_calls,
                "next_action": "",
                "next_input": "",
                "answer": "",
                "input_tokens": 0,
                "output_tokens": 0,
            }
        )
        elapsed = time.perf_counter() - start

        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)

        return RunResult(
            answer=Answer(
                question_id="",
                text=result.get("answer", ""),
                sources_used=result.get("sources", []),
                metadata={
                    "mode": self._mode,
                    "query_trace": result.get("sql_trace", []) + result.get("doc_trace", []),
                    "sql_trace": result.get("sql_trace", []),
                    "doc_trace": result.get("doc_trace", []),
                    "tool_trace": result.get("tool_trace", []),
                    "tool_calls": int(result.get("tool_calls", 0)),
                },
            ),
            usage=UsageStats(
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                latency_seconds=elapsed,
                model_name=self._model,
            ),
        )

    async def cleanup(self) -> None:
        """Release chromadb and sqlite resources."""
        if self._embedding_store is None and self._collection is not None:
            self._chroma_client.delete_collection(self._collection_name)
            self._collection = None
        if self._conn is not None:
            self._conn.close()
            self._conn = None
        self._graph = None
