"""Evaluation harness for framework benchmarking.

Modules:
    harness: Orchestrates ingest, query, judge, and aggregate.
    llm_judge: LLM-as-judge for answer quality.
    code_quality: Static code metrics via radon and ast.
    code_review: LLM-as-judge for implementation code quality.
    metrics: Token cost estimation.
    retrieval: Precision and recall.
    profiles: Scenario-specific metric extensions (e.g. multi-hop chain coverage).
"""
