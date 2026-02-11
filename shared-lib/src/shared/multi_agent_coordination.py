"""Shared runtime for the multi_agent_coordination scenario tools.

This module centralizes tool semantics so framework implementations can focus on
native multi-agent orchestration while sharing identical underlying behavior.

Three specialist domains with distinct tools:
- Infrastructure: query_infrastructure() — SQL on infra tables
- Security: query_security() — SQL on security tables
- Runbook: lookup_runbook() — semantic search over policy docs
"""

from __future__ import annotations

import json
import re
import sqlite3
import threading
import uuid
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

import chromadb
from openai import OpenAI

from shared.interface import Document
from shared.retrieval import EmbeddingStore, RetrievalResult, chunk_text

EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4
PROMPT_VERSION = "multi_agent_coord.v1"

# Tables accessible per domain.  incidents and incident_timeline are shared.
INFRA_TABLES = {
    "clusters", "services", "dependencies", "recent_deploys",
    "incidents", "incident_timeline",
}
SECURITY_TABLES = {
    "vulnerability_scans", "access_logs", "firewall_rules",
    "incidents", "incident_timeline",
}

# Canonical tool descriptions — used by all framework implementations to
# ensure the LLM receives identical guidance regardless of framework.
QUERY_INFRASTRUCTURE_DESC = (
    "Execute read-only SQL (SELECT/WITH/PRAGMA) on infrastructure tables: "
    "clusters, services, dependencies, recent_deploys, incidents, incident_timeline."
)
QUERY_SECURITY_DESC = (
    "Execute read-only SQL (SELECT/WITH/PRAGMA) on security tables: "
    "vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline."
)
LOOKUP_RUNBOOK_DESC = (
    "Search operational runbooks and policy documents for relevant evidence."
)
CONSULT_INFRASTRUCTURE_DESC = (
    "Consult the infrastructure specialist. Ask questions about servers, "
    "clusters, deployments, service dependencies, and infrastructure state."
)
CONSULT_SECURITY_DESC = (
    "Consult the security specialist. Ask questions about vulnerabilities, "
    "access logs, firewall rules, and security compliance."
)
CONSULT_RUNBOOK_DESC = (
    "Consult the runbook specialist. Ask questions about change management "
    "policies, incident response procedures, SLAs, and compliance rules."
)

COORDINATOR_PROMPT = (
    "You are an incident-response coordinator at NimbusOps.\n"
    "You have access to three specialist tools:\n"
    "- query_infrastructure(sql): read-only SQL on infrastructure tables "
    "(clusters, services, dependencies, recent_deploys, incidents, incident_timeline)\n"
    "- query_security(sql): read-only SQL on security tables "
    "(vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline)\n"
    "- lookup_runbook(query): semantic search over operational policies and runbooks\n\n"
    "Use schema introspection (PRAGMA table_info) when column names are uncertain.\n"
    "Combine evidence from multiple domains to build a grounded answer.\n"
    "If evidence is missing or conflicting, state what is missing."
)

INFRA_SPECIALIST_PROMPT = (
    "You are an infrastructure specialist at NimbusOps.\n"
    "You have access to query_infrastructure(sql) for read-only SQL on: "
    "clusters, services, dependencies, recent_deploys, incidents, incident_timeline.\n"
    "Focus on server state, service health, deployment history, and dependency chains.\n"
    "Use PRAGMA table_info() to discover column names when uncertain."
)

SECURITY_SPECIALIST_PROMPT = (
    "You are a security specialist at NimbusOps.\n"
    "You have access to query_security(sql) for read-only SQL on: "
    "vulnerability_scans, access_logs, firewall_rules, incidents, incident_timeline.\n"
    "Focus on vulnerabilities, anomalous access patterns, firewall rule changes, and compliance.\n"
    "Use PRAGMA table_info() to discover column names when uncertain."
)

RUNBOOK_SPECIALIST_PROMPT = (
    "You are an operations specialist at NimbusOps.\n"
    "You have access to lookup_runbook(query) for semantic search over policy documents.\n"
    "Focus on change management rules, incident response procedures, SLAs, and compliance policies.\n"
    "Provide specific policy references in your answers."
)


@dataclass(frozen=True)
class ToolTraceEntry:
    tool: str
    domain: str
    input: str
    sources: list[str]


def get_coordinator_prompt() -> str:
    """Return the shared coordinator system prompt."""
    return COORDINATOR_PROMPT


def get_specialist_prompt(domain: str) -> str:
    """Return the specialist system prompt for a domain."""
    prompts = {
        "infrastructure": INFRA_SPECIALIST_PROMPT,
        "security": SECURITY_SPECIALIST_PROMPT,
        "runbook": RUNBOOK_SPECIALIST_PROMPT,
    }
    return prompts.get(domain, COORDINATOR_PROMPT)


def get_coordinator_prompt_hash() -> str:
    """Stable hash to audit prompt parity across framework runs."""
    return sha256(COORDINATOR_PROMPT.encode("utf-8")).hexdigest()[:12]


def build_task_prompt(question: str, max_tool_calls: int) -> str:
    """Return a shared task prompt that keeps per-run budget explicit."""
    return (
        f"Question: {question}\n"
        f"Tool budget: at most {max(1, max_tool_calls)} calls.\n"
        "Use tools as needed and provide a grounded final answer."
    )


class MultiAgentRuntime:
    """Runtime backing specialist tools for the multi_agent_coordination scenario."""

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
            self._collection_name = f"multi_agent_docs_{uuid.uuid4().hex[:8]}"
        else:
            self._chroma_client = None
            self._openai_client = None
            self._collection = None
            self._collection_name = None

        self._max_tool_calls = 0
        self._tool_calls = 0
        self._tool_trace: list[ToolTraceEntry] = []
        self._sources_used: list[str] = []

    # -- Lifecycle ---------------------------------------------------------

    def set_limits(self, *, top_k: int, max_context_chunks: int) -> None:
        self._top_k = top_k
        self._max_context_chunks = max_context_chunks

    def start_run(self, *, max_tool_calls: int) -> None:
        self._max_tool_calls = max(1, max_tool_calls)
        self._tool_calls = 0
        self._tool_trace = []
        self._sources_used = []

    # -- Observation -------------------------------------------------------

    def tool_calls(self) -> int:
        return self._tool_calls

    def tool_trace(self) -> list[dict[str, str | list[str]]]:
        return [
            {
                "tool": e.tool,
                "domain": e.domain,
                "input": e.input,
                "sources": list(e.sources),
            }
            for e in self._tool_trace
        ]

    def sources_used(self) -> list[str]:
        return list(self._sources_used)

    def agents_used(self) -> list[str]:
        """Return deduplicated ordered list of specialist domains invoked."""
        seen: set[str] = set()
        result: list[str] = []
        for entry in self._tool_trace:
            if entry.domain not in seen:
                seen.add(entry.domain)
                result.append(entry.domain)
        return result

    # -- Internal helpers --------------------------------------------------

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

    def _record_call(
        self, *, tool: str, domain: str, tool_input: str, sources: list[str]
    ) -> None:
        self._tool_trace.append(
            ToolTraceEntry(tool=tool, domain=domain, input=tool_input, sources=sources)
        )
        self._add_sources(sources)

    def _consume_tool_call(self, tool: str, domain: str, tool_input: str) -> str | None:
        if self._tool_calls >= self._max_tool_calls:
            self._record_call(tool=tool, domain=domain, tool_input=tool_input, sources=[])
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

    def _schema_brief(self, allowed_tables: set[str] | None = None) -> str:
        with self._lock:
            if self._conn is None:
                return "Schema unavailable."
            tables = [
                str(row["name"])
                for row in self._conn.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
                ).fetchall()
            ]
            if allowed_tables is not None:
                tables = [t for t in tables if t.lower() in allowed_tables]
            if not tables:
                return "No accessible tables."
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

    def _run_scoped_sql(
        self, query: str, domain: str, allowed_tables: set[str]
    ) -> str:
        """Execute SQL scoped to a set of allowed tables for a domain."""
        tool_name = f"query_{domain}"
        with self._lock:
            budget_error = self._consume_tool_call(tool_name, domain, query)
            if budget_error:
                return budget_error

            if self._conn is None:
                self._record_call(
                    tool=tool_name, domain=domain, tool_input=query, sources=[]
                )
                return "Database not initialized."

            cleaned = query.strip().rstrip(";")
            if not cleaned:
                self._record_call(
                    tool=tool_name, domain=domain, tool_input=query, sources=[]
                )
                return "Empty SQL query."

            if not self._is_safe_sql(cleaned):
                hint = self._schema_brief(allowed_tables)
                self._record_call(
                    tool=tool_name, domain=domain, tool_input=query, sources=[]
                )
                return (
                    "Unsafe or unsupported SQL. Only SELECT/WITH/PRAGMA read-only "
                    f"queries are allowed.\nAccessible tables:\n{hint}"
                )

            try:
                cursor = self._conn.execute(cleaned)
                rows = [dict(row) for row in cursor.fetchall()]
                row_count = len(rows)
                payload = json.dumps(rows[:20], indent=2, default=str)

                sources = self._extract_sql_sources(cleaned)
                known = self._known_tables()
                sources = [s for s in sources if s in known]

                lowered = cleaned.lower()
                if lowered.startswith("pragma table_info("):
                    match = re.search(
                        r"pragma\s+table_info\(([^)]+)\)", lowered
                    )
                    if match:
                        table = match.group(1).strip().strip("'\"").lower()
                        if table in known:
                            sources = self._merge_unique(sources, [table])

                self._record_call(
                    tool=tool_name, domain=domain, tool_input=query, sources=sources
                )
                return f"Row count: {row_count}\nRows (max 20):\n{payload}"
            except Exception as err:
                hint = self._schema_brief(allowed_tables)
                self._record_call(
                    tool=tool_name, domain=domain, tool_input=query, sources=[]
                )
                return f"SQL error: {err}\nAccessible tables:\n{hint}"

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

    # -- Public lifecycle --------------------------------------------------

    def prepare(self, documents: list[Document]) -> None:
        """Initialize database and document embeddings."""
        self._init_db()
        if self._embedding_store is not None:
            return

        openai_client = self._ensure_openai()
        self._collection = self._chroma_client.create_collection(
            name=self._collection_name
        )

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

    def cleanup(self) -> None:
        """Release database and embedding resources."""
        with self._lock:
            if self._embedding_store is None and self._collection is not None:
                self._chroma_client.delete_collection(self._collection_name)
                self._collection = None
            if self._conn is not None:
                self._conn.close()
                self._conn = None

    # -- Tools exposed to frameworks ---------------------------------------

    def query_infrastructure(self, query: str) -> str:
        """Execute read-only SQL scoped to infrastructure tables."""
        return self._run_scoped_sql(query, "infrastructure", INFRA_TABLES)

    def query_security(self, query: str) -> str:
        """Execute read-only SQL scoped to security tables."""
        return self._run_scoped_sql(query, "security", SECURITY_TABLES)

    def lookup_runbook(self, query: str) -> str:
        """Semantic search over operational runbooks and policy documents."""
        with self._lock:
            budget_error = self._consume_tool_call("lookup_runbook", "runbook", query)
            if budget_error:
                return budget_error

            retrieval = self._retrieve_docs(query)
            chunks = retrieval.chunks[: self._max_context_chunks]
            if not chunks:
                self._record_call(
                    tool="lookup_runbook",
                    domain="runbook",
                    tool_input=query,
                    sources=[],
                )
                return "No policy/document context found."

            self._record_call(
                tool="lookup_runbook",
                domain="runbook",
                tool_input=query,
                sources=list(retrieval.sources),
            )
            return "\n\n---\n\n".join(chunks)
