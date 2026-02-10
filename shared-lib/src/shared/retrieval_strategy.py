"""Reusable retrieval strategies for baseline and capability benchmark modes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

from shared.retrieval import RetrievalResult


@dataclass(frozen=True)
class RetrievalStrategyConfig:
    """Controls iterative retrieval for capability mode."""

    top_k: int = 3
    retrieval_rounds: int = 1
    max_context_chunks: int = 3
    max_followup_queries: int = 3


@dataclass(frozen=True)
class IterativeRetrievalResult:
    """Retrieval output with query trace for diagnostics/benchmarking."""

    retrieval: RetrievalResult
    query_trace: list[str]


def _extract_entities(text: str) -> list[str]:
    entities: set[str] = set()
    for match in re.findall(r"\bprod-api-\d{2}\b", text, flags=re.IGNORECASE):
        entities.add(match.lower())
    for match in re.findall(r"\bR-\d{3}\b", text, flags=re.IGNORECASE):
        entities.add(match.upper())
    for match in re.findall(r"\bINC-\d{4}-\d{3}\b", text, flags=re.IGNORECASE):
        entities.add(match.upper())
    for match in re.findall(r"\b(?:us-west|us-east|us-central)\b", text, flags=re.IGNORECASE):
        entities.add(match.lower())
    for match in re.findall(r"\bProject\s+([A-Z][a-zA-Z0-9_-]+)\b", text):
        entities.add(f"project {match.lower()}")
    return sorted(entities)


def _build_followup_queries(question: str, chunks: list[str], max_queries: int) -> list[str]:
    combined = "\n".join(chunks)
    entities = _extract_entities(question) + _extract_entities(combined)

    queries: list[str] = []
    for entity in entities:
        if entity.startswith("prod-api-"):
            queries.append(f"{entity} project owner rack datacenter")
        elif entity.startswith("R-"):
            queries.append(f"{entity} datacenter rack range mapping")
        elif entity.startswith("INC-"):
            queries.append(f"{entity} affected server root cause")
        elif entity.startswith("project "):
            queries.append(f"{entity} server and owning team")
        elif entity.startswith("us-"):
            queries.append(f"{entity} SLA tier uptime guarantee")
        else:
            queries.append(f"{entity} details")

    if "datacenter" in question.lower():
        queries.append(f"{question} rack mapping")
    if "on-call" in question.lower():
        queries.append(f"{question} owning team")

    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        key = query.lower().strip()
        if key and key not in seen:
            seen.add(key)
            deduped.append(query)
        if len(deduped) >= max_queries:
            break
    return deduped


def iterative_retrieve(
    question: str,
    retrieve_fn: Callable[[str, int], RetrievalResult],
    config: RetrievalStrategyConfig,
) -> IterativeRetrievalResult:
    """Retrieve context with optional iterative follow-up queries."""
    if config.retrieval_rounds <= 1:
        retrieval = retrieve_fn(question, config.top_k)
        chunks = retrieval.chunks[: config.max_context_chunks]
        sources: list[str] = []
        for source in retrieval.sources:
            if source not in sources:
                sources.append(source)
        return IterativeRetrievalResult(
            retrieval=RetrievalResult(chunks=chunks, sources=sources),
            query_trace=[question],
        )

    all_chunks: list[str] = []
    all_sources: list[str] = []
    seen_chunks: set[str] = set()
    seen_queries: set[str] = set()

    pending_queries = [question]
    query_trace: list[str] = []

    for _ in range(config.retrieval_rounds):
        if not pending_queries:
            break

        round_queries: list[str] = []
        for query in pending_queries:
            key = query.lower().strip()
            if key not in seen_queries:
                seen_queries.add(key)
                round_queries.append(query)
            if len(round_queries) >= config.max_followup_queries:
                break

        if not round_queries:
            break

        for query in round_queries:
            retrieval = retrieve_fn(query, config.top_k)
            query_trace.append(query)
            for chunk in retrieval.chunks:
                if chunk not in seen_chunks and len(all_chunks) < config.max_context_chunks:
                    seen_chunks.add(chunk)
                    all_chunks.append(chunk)
            for source in retrieval.sources:
                if source not in all_sources:
                    all_sources.append(source)

        pending_queries = _build_followup_queries(
            question=question,
            chunks=all_chunks,
            max_queries=config.max_followup_queries,
        )

    return IterativeRetrievalResult(
        retrieval=RetrievalResult(chunks=all_chunks, sources=all_sources),
        query_trace=query_trace,
    )
