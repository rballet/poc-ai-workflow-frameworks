"""Retrieval quality metrics."""


def retrieval_precision(retrieved: list[str], relevant: list[str]) -> float:
    """What fraction of retrieved docs are relevant?"""
    if not retrieved:
        return 0.0
    relevant_set = set(relevant)
    hits = sum(1 for doc in retrieved if doc in relevant_set)
    return hits / len(retrieved)


def retrieval_recall(retrieved: list[str], relevant: list[str]) -> float:
    """What fraction of relevant docs were retrieved?"""
    if not relevant:
        return 1.0
    retrieved_set = set(retrieved)
    hits = sum(1 for doc in relevant if doc in retrieved_set)
    return hits / len(relevant)
