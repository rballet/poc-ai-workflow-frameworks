# Benchmark Results Summary

This file summarizes the latest benchmark findings and links to the detailed reports.

## Referenced Reports

- Multi-hop baseline: [`results/comparison_multihop_qa_baseline.md`](results/comparison_multihop_qa_baseline.md)
- Multi-hop capability: [`results/comparison_multihop_qa_capability.md`](results/comparison_multihop_qa_capability.md)
- RAG baseline: [`results/comparison_rag_qa_baseline.md`](results/comparison_rag_qa_baseline.md)
- Metric definitions: [`METRICS.md`](METRICS.md)

## Main Findings

- Baseline mode is mostly parity-focused and keeps framework differences smaller.
- Capability mode now exposes real framework tradeoffs for multi-hop chaining:
  - quality and hop coverage generally improve,
  - but cost/latency can increase significantly.

## Why Frameworks Differ On Multi-hop

- Pydantic AI
  - Strength: structured planner + sufficiency-check loop improves recall with controlled behavior.
  - Limitation: can still miss difficult bridge mappings (for example, rack-to-datacenter edge cases).
- LangGraph
  - Strength: explicit graph loop (`retrieve -> assess -> retrieve/generate`) is robust for iterative evidence gathering.
  - Limitation: extra graph iterations can inflate token and latency budgets.
- smolagents
  - Strength: tool-driven agent loop is very good at deep multi-step exploration and often reaches highest chain coverage.
  - Limitation: highest orchestration overhead (substantially more tokens/time) and requires strict budget controls.

## Scenario-level Interpretation

- For simple RAG QA, all frameworks can be effective with low complexity.
- For multi-hop QA, framework orchestration style matters more than single-pass retrieval quality.
- If your priority is best answer quality under loose budgets, the most agentic approach can win.
- If your priority is predictable cost/latency, structured or graph-based loops are generally easier to control.
