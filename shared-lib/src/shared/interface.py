"""Standard interface that every framework implementation must satisfy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Document:
    """A document for the knowledge base."""

    content: str
    source: str
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Question:
    """A test question with expected answer for evaluation."""

    id: str
    text: str
    expected_answer: str
    expected_sources: list[str] = field(default_factory=list)


@dataclass
class Answer:
    """An answer produced by a framework."""

    question_id: str
    text: str
    sources_used: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class UsageStats:
    """Token usage and timing from a single run."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_seconds: float = 0.0
    model_name: str = ""


@dataclass
class RunResult:
    """Complete result from answering one question."""

    answer: Answer
    usage: UsageStats


@runtime_checkable
class RAGFramework(Protocol):
    """Protocol that every RAG framework implementation must satisfy."""

    @property
    def name(self) -> str:
        """Human-readable framework name, e.g. 'LangGraph 1.0.8'."""
        ...

    async def ingest(self, documents: list[Document]) -> None:
        """Load documents into the framework's retrieval system."""
        ...

    async def query(self, question: str) -> RunResult:
        """Answer a question using ingested documents."""
        ...

    async def cleanup(self) -> None:
        """Release resources (vector store, connections, etc.)."""
        ...
