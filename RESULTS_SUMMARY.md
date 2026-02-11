# Benchmark Results Summary

This file summarizes the latest benchmark findings and links to the detailed reports.

## Referenced Reports

- Multi-hop baseline: [`results/comparison_multihop_qa_baseline.md`](results/comparison_multihop_qa_baseline.md)
- Multi-hop capability: [`results/comparison_multihop_qa_capability.md`](results/comparison_multihop_qa_capability.md)
- RAG baseline: [`results/comparison_rag_qa_baseline.md`](results/comparison_rag_qa_baseline.md)
- Agentic SQL baseline: [`results/comparison_agentic_sql_qa_baseline.md`](results/comparison_agentic_sql_qa_baseline.md)
- Agentic SQL capability: [`results/comparison_agentic_sql_qa_capability.md`](results/comparison_agentic_sql_qa_capability.md)
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
  - Limitation: highest orchestration overhead (substantially more tokens/time). Much of this overhead is due to GPT-5-mini not supporting the `stop` parameter that smolagents relies on for step control, causing inefficient token usage and frequent step exhaustion. Results with a compatible model (e.g. gpt-4o-mini) would likely show significantly better efficiency.

## Scenario-level Interpretation

- For simple RAG QA, all frameworks can be effective with low complexity.
- For multi-hop QA, framework orchestration style matters more than single-pass retrieval quality.
- If your priority is best answer quality under loose budgets, the most agentic approach can win.
- If your priority is predictable cost/latency, structured or graph-based loops are generally easier to control.

## Latest Findings: Agentic SQL (Capability)

- Best overall balance in this scenario: **Pydantic AI**.
  - Strong quality (`correctness/completeness/faithfulness`) with lower latency/cost than alternatives.
  - Why it works well here: native tool loop stays efficient while still grounding decisions in SQL + docs.
- **LangGraph** is close on efficiency but less consistent on hard branching outcomes in this run.
  - Why: graph loop is robust, but additional iterations/tool turns can amplify variance on decision-heavy questions.
- **smolagents** remains the most expensive/slow path in this scenario configuration.
  - Why: smolagents relies on the `stop` parameter to control its agent step loop, but GPT-5-mini is a reasoning model that [does not support stop sequences](https://community.openai.com/t/why-doesnt-gpt-5-1-support-stop-sequences/1366800). This causes inefficient step usage, frequent `max_steps` exhaustion, and timeouts. This is a known framework-model incompatibility ([smolagents #1893](https://github.com/huggingface/smolagents/issues/1893)), not a reflection of smolagents' capability with compatible models (e.g. gpt-4o-mini).
  - It can still perform well on some complex questions (e.g. multihop_qa capability where it scores highest), but latency and token overhead remain significantly higher due to this limitation.

### Artifacts used for this summary

- Pydantic AI run: [`results/pydantic_ai_agentic_sql_qa_20260211_174017.json`](results/pydantic_ai_agentic_sql_qa_20260211_174017.json)
- LangGraph run: [`results/langgraph_agentic_sql_qa_20260211_174355.json`](results/langgraph_agentic_sql_qa_20260211_174355.json)
- smolagents run (latest completed full-metrics artifact): [`results/smolagents_agentic_sql_qa_20260211_171939.json`](results/smolagents_agentic_sql_qa_20260211_171939.json)
