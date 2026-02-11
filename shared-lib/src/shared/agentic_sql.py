"""Shared runtime for the agentic_sql_qa scenario tools.

This module centralizes tool semantics so framework implementations can focus on
native tool-calling orchestration while sharing identical underlying behavior.
"""

from __future__ import annotations

import json
import re
import sqlite3
import threading
import uuid
from hashlib import sha256
from dataclasses import dataclass
from pathlib import Path

import chromadb
from openai import OpenAI

from shared.interface import Document
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
PROMPT_VERSION = "agentic_sql.v2"
# Canonical tool descriptions — used by all framework implementations to
# ensure the LLM receives identical guidance regardless of framework.
RUN_SQL_DESC = (
    "Execute read-only SQL (SELECT/WITH/PRAGMA) against the scenario SQLite database."
)
LOOKUP_DOC_DESC = (
    "Search scenario policy/process documents for relevant evidence."
)

SYSTEM_PROMPT = (
    "You are a tool-using analyst for customer support operations.\n"
    "Answer only from tool evidence. Do not invent facts.\n\n"
    "Tools:\n"
    "- run_sql(query): read-only SQL on local SQLite data; supports SELECT, WITH, and PRAGMA.\n"
    "- lookup_doc(query): semantic search over policy/process markdown docs.\n\n"
    "Reasoning policy:\n"
    "- Use schema introspection with PRAGMA when table/column names are uncertain.\n"
    "- Choose tool calls based on what evidence is needed for the question.\n"
    "- Prefer the minimal set of tool calls needed for a grounded answer.\n"
    "- If evidence is missing or conflicting, state what is missing."
)


@dataclass(frozen=True)
class ToolTraceEntry:
    tool: str
    input: str
    sources: list[str]


def get_system_prompt() -> str:
    """Return the shared system prompt used across frameworks for fair comparison."""
    return SYSTEM_PROMPT


def get_system_prompt_hash() -> str:
    """Stable hash to audit prompt parity across framework runs."""
    return sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest()[:12]


def build_task_prompt(question: str, max_tool_calls: int) -> str:
    """Return a shared task prompt that keeps per-run budget explicit."""
    return (
        f"Question: {question}\n"
        f"Tool budget: at most {max(1, max_tool_calls)} calls.\n"
        "Use tools as needed and provide a grounded final answer."
    )


class AgenticSQLRuntime:
    """Runtime backing `run_sql` and `lookup_doc` tools for agentic_sql_qa."""

    def __init__(
        self,
        *,
        scenario_name: str,
        database_seed_file: str,
        embedding_store: EmbeddingStore | None,
        embedding_model: str = EMBEDDING_MODEL,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        top_k: int = TOP_K,
        max_context_chunks: int = TOP_K,
    ) -> None:
        self._scenario_name = scenario_name
        self._database_seed_file = database_seed_file
        self._embedding_store = embedding_store
        self._embedding_model = embedding_model
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._top_k = top_k
        self._max_context_chunks = max_context_chunks

        self._conn: sqlite3.Connection | None = None
        self._lock = threading.RLock()

        if embedding_store is None:
            self._chroma_client = chromadb.Client()
            self._openai_client: OpenAI | None = None
            self._collection: chromadb.Collection | None = None
            self._collection_name = f"agentic_sql_docs_{uuid.uuid4().hex[:8]}"
        else:
            self._chroma_client = None
            self._openai_client = None
            self._collection = None
            self._collection_name = None

        self._max_tool_calls = 0
        self._tool_calls = 0
        self._tool_trace: list[ToolTraceEntry] = []
        self._sources_used: list[str] = []

    def set_limits(self, *, top_k: int, max_context_chunks: int) -> None:
        self._top_k = top_k
        self._max_context_chunks = max_context_chunks

    def start_run(self, *, max_tool_calls: int) -> None:
        self._max_tool_calls = max(1, max_tool_calls)
        self._tool_calls = 0
        self._tool_trace = []
        self._sources_used = []

    def tool_calls(self) -> int:
        return self._tool_calls

    def tool_trace(self) -> list[dict[str, str | list[str]]]:
        return [
            {"tool": entry.tool, "input": entry.input, "sources": list(entry.sources)}
            for entry in self._tool_trace
        ]

    def sources_used(self) -> list[str]:
        return list(self._sources_used)

    def _resolve_seed_sql_path(self) -> Path:
        repo_root = Path(__file__).resolve().parents[3]
        return repo_root / "scenarios" / self._scenario_name / self._database_seed_file

    def _ensure_openai(self) -> OpenAI:
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _init_db(self) -> None:
        seed_path = self._resolve_seed_sql_path()
        if not seed_path.exists():
            raise FileNotFoundError(f"SQLite seed file not found: {seed_path}")
        with self._lock:
            if self._conn is not None:
                self._conn.close()
            self._conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.executescript(seed_path.read_text())
            self._conn.commit()

    @staticmethod
    def _merge_unique(existing: list[str], incoming: list[str]) -> list[str]:
        merged = list(existing)
        seen = set(existing)
        for item in incoming:
            if item not in seen:
                seen.add(item)
                merged.append(item)
        return merged

    def _add_sources(self, sources: list[str]) -> None:
        self._sources_used = self._merge_unique(self._sources_used, sources)

    def _record_call(self, *, tool: str, tool_input: str, sources: list[str]) -> None:
        self._tool_trace.append(ToolTraceEntry(tool=tool, input=tool_input, sources=sources))
        self._add_sources(sources)

    def _consume_tool_call(self, tool: str, tool_input: str) -> str | None:
        if self._tool_calls >= self._max_tool_calls:
            self._record_call(tool=tool, tool_input=tool_input, sources=[])
            return (
                f"Tool-call budget exhausted ({self._max_tool_calls}). "
                "Proceed with collected evidence."
            )
        self._tool_calls += 1
        return None

    def _known_tables(self) -> set[str]:
        with self._lock:
            if self._conn is None:
                return set()
            return {
                str(row["name"]).lower()
                for row in self._conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
            }

    def _schema_brief(self) -> str:
        with self._lock:
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
                cols = self._conn.execute(f"PRAGMA table_info({table})").fetchall()
                col_names = [str(row["name"]) for row in cols]
                lines.append(f"{table}: {', '.join(col_names)}")
            return "\n".join(lines)

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
            lowered = table.lower()
            if lowered not in seen:
                seen.add(lowered)
                deduped.append(lowered)
        return deduped

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
        return (
            lowered.startswith("select")
            or lowered.startswith("with")
            or lowered.startswith("pragma")
        )

    def _retrieve_docs(self, query: str) -> RetrievalResult:
        if self._embedding_store is not None:
            return self._embedding_store.retrieve(query, top_k=self._top_k)

        openai_client = self._ensure_openai()
        response = openai_client.embeddings.create(
            model=self._embedding_model,
            input=query,
        )
        query_embedding = response.data[0].embedding

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=self._top_k,
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

    def prepare(self, documents: list[Document]) -> None:
        self._init_db()
        if self._embedding_store is not None:
            return

        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(name=self._collection_name)

        all_chunks: list[str] = []
        all_ids: list[str] = []
        all_metadatas: list[dict[str, str]] = []
        for doc in documents:
            chunks = chunk_text(doc.content, self._chunk_size, self._chunk_overlap)
            for i, text in enumerate(chunks):
                all_chunks.append(text)
                all_ids.append(f"{doc.source}_{i}")
                all_metadatas.append({"source": doc.source})

        response = openai_client.embeddings.create(
            model=self._embedding_model,
            input=all_chunks,
        )
        embeddings = [item.embedding for item in response.data]
        self._collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
        )

    def run_sql(self, query: str) -> str:
        """Tool: execute read-only SQL and return textual observation."""
        with self._lock:
            budget_error = self._consume_tool_call("run_sql", query)
            if budget_error:
                return budget_error

            if self._conn is None:
                observation = "Database not initialized."
                self._record_call(tool="run_sql", tool_input=query, sources=[])
                return observation

            cleaned = query.strip().rstrip(";")
            if not cleaned:
                observation = "Empty SQL query."
                self._record_call(tool="run_sql", tool_input=query, sources=[])
                return observation
            if not self._is_safe_sql(cleaned):
                observation = (
                    "Unsafe or unsupported SQL. Only SELECT/WITH/PRAGMA read-only "
                    f"queries are allowed.\nSchema hint:\n{self._schema_brief()}"
                )
                self._record_call(tool="run_sql", tool_input=query, sources=[])
                return observation

            try:
                cursor = self._conn.execute(cleaned)
                rows = [dict(row) for row in cursor.fetchall()]
                row_count = len(rows)
                payload = json.dumps(rows[:20], indent=2, default=str)

                sources = self._extract_sql_sources(cleaned)
                known = self._known_tables()
                sources = [source for source in sources if source in known]

                lowered = cleaned.lower()
                if lowered.startswith("pragma table_info("):
                    match = re.search(r"pragma\s+table_info\(([^)]+)\)", lowered)
                    if match:
                        table = match.group(1).strip().strip("'\"").lower()
                        if table in known:
                            sources = self._merge_unique(sources, [table])

                self._record_call(tool="run_sql", tool_input=query, sources=sources)
                return f"Row count: {row_count}\nRows (max 20):\n{payload}"
            except Exception as err:
                observation = f"SQL error: {err}\nSchema hint:\n{self._schema_brief()}"
                self._record_call(tool="run_sql", tool_input=query, sources=[])
                return observation

    def lookup_doc(self, query: str) -> str:
        """Tool: semantic search over scenario documents."""
        with self._lock:
            budget_error = self._consume_tool_call("lookup_doc", query)
            if budget_error:
                return budget_error

            retrieval = self._retrieve_docs(query)
            chunks = retrieval.chunks[: self._max_context_chunks]
            if not chunks:
                self._record_call(tool="lookup_doc", tool_input=query, sources=[])
                return "No policy/document context found."

            self._record_call(
                tool="lookup_doc",
                tool_input=query,
                sources=list(retrieval.sources),
            )
            return "\n\n---\n\n".join(chunks)

    def cleanup(self) -> None:
        with self._lock:
            if self._embedding_store is None and self._collection is not None:
                self._chroma_client.delete_collection(self._collection_name)
                self._collection = None
            if self._conn is not None:
                self._conn.close()
                self._conn = None
