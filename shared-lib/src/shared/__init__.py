"""Shared interfaces and evaluation harness for AI framework benchmarking."""

from shared.interface import (
    Answer,
    ConfigurableFramework,
    Document,
    Question,
    RAGFramework,
    RunResult,
    UsageStats,
)

__all__ = [
    "Answer",
    "ConfigurableFramework",
    "Document",
    "Question",
    "RAGFramework",
    "RunResult",
    "UsageStats",
]
