"""Shared interfaces and evaluation harness for AI framework benchmarking."""

from shared.interface import (
    Answer,
    Document,
    Question,
    RAGFramework,
    RunResult,
    UsageStats,
)

__all__ = [
    "Answer",
    "Document",
    "Question",
    "RAGFramework",
    "RunResult",
    "UsageStats",
]
