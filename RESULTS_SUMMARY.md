# Benchmark Results Summary

This file summarizes the latest benchmark findings and links to the detailed reports.

## Referenced Reports

- RAG baseline: [`results/comparison_rag_qa_baseline.md`](results/comparison_rag_qa_baseline.md)
- Multi-hop baseline: [`results/comparison_multihop_qa_baseline.md`](results/comparison_multihop_qa_baseline.md)
- Multi-hop capability: [`results/comparison_multihop_qa_capability.md`](results/comparison_multihop_qa_capability.md)
- Agentic SQL baseline: [`results/comparison_agentic_sql_qa_baseline.md`](results/comparison_agentic_sql_qa_baseline.md)
- Agentic SQL capability: [`results/comparison_agentic_sql_qa_capability.md`](results/comparison_agentic_sql_qa_capability.md)
- Multi-agent coordination baseline: [`results/comparison_multi_agent_coordination_baseline.md`](results/comparison_multi_agent_coordination_baseline.md)
- Multi-agent coordination capability: [`results/comparison_multi_agent_coordination_capability.md`](results/comparison_multi_agent_coordination_capability.md)
- Metric definitions: [`METRICS.md`](METRICS.md)

## Main Findings

- Baseline mode is mostly parity-focused and keeps framework differences smaller.
- Capability mode exposes real framework tradeoffs across all scenarios:
  - quality and hop/agent coverage generally improve,
  - but cost/latency can increase significantly.
- **Multi-agent coordination is the most differentiating scenario.** It requires frameworks to orchestrate multiple specialist agents (infra, security, runbook) with a shared tool budget, exposing fundamental differences in how each framework handles multi-agent delegation, evidence synthesis, and budget management. The gap between frameworks is much larger here than in simpler scenarios.

## Why Frameworks Differ

### On Multi-hop QA

- **Pydantic AI**: structured planner + sufficiency-check loop improves recall with controlled behavior. Can still miss difficult bridge mappings (e.g. rack-to-datacenter edge cases).
- **LangGraph**: explicit graph loop (`retrieve -> assess -> retrieve/generate`) is robust for iterative evidence gathering. Extra graph iterations can inflate token and latency budgets.
- **smolagents**: tool-driven agent loop is very good at deep multi-step exploration and often reaches highest chain coverage. Highest orchestration overhead (more tokens/time) due to GPT-5-mini not supporting the `stop` parameter.

### On Multi-Agent Coordination

- **Pydantic AI** (4.5/5 capability correctness)
  - Strength: agent-as-tool pattern lets the coordinator call specialist sub-agents as functions. Each specialist runs with its own prompt and tool access, then returns structured results to the coordinator. This cleanly separates domain concerns and allows the coordinator to synthesize evidence from multiple specialists.
  - Result: 100% agent coverage, 100% tool coverage, 85.8% hop coverage. Scored 5/5 on all 3 easy questions and 4-5/5 on most coordination questions.
- **LangGraph** (3.4/5 capability correctness)
  - Strength: supervisor graph with conditional routing can delegate to specialist nodes. Graph structure is explicit and auditable.
  - Limitation: with the default 5-minute query timeout, the hardest coordination questions (q8, q10) timed out at 300s. The supervisor sometimes under-delegates, using only 1-2 specialists when 3 are needed, resulting in 68.3% agent coverage. Scored 5/5 on easy questions but dropped to 0-2/5 on hard coordination.
- **smolagents** (0.4/5 capability correctness)
  - Limitation: fundamentally broken on this scenario with GPT-5-mini. The `stop` parameter incompatibility causes step control failures, and OpenAI 500 errors on long queries compound the problem. 8 out of 10 questions timed out or errored. This is a framework-model incompatibility, not a reflection of smolagents' architecture.

## Scenario-level Interpretation

- For **simple RAG QA**, all frameworks can be effective with low complexity.
- For **multi-hop QA**, framework orchestration style matters more than single-pass retrieval quality.
- For **agentic SQL QA**, tool loop efficiency and error handling determine success.
- For **multi-agent coordination**, the ability to delegate to and synthesize from multiple specialist agents is the primary differentiator. This is where framework architecture matters most.
- If your priority is best answer quality under loose budgets, the most agentic approach can win.
- If your priority is predictable cost/latency, structured or graph-based loops are generally easier to control.

## Latest Findings: Multi-Agent Coordination

### Capability Mode

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Correctness (1-5) | **4.5** | 3.4 | 0.4 |
| Avg Completeness (1-5) | **4.1** | 3.2 | 0.4 |
| Avg Faithfulness (1-5) | **4.7** | 3.5 | 0.4 |
| Avg Latency (s) | **95.6** | 137.3 | 241.6 |
| Total Tokens | 331,585 | 310,753 | 0 |
| Est. Cost (USD) | $0.30 | $0.18 | $0.00 |
| Hop Coverage | 85.8% | 66.7% | 0% |
| Agent Coverage | 100% | 68.3% | 25% |
| Coordination Success Rate | 42.9% | 28.6% | 0% |

#### Per-Question Correctness

| Question | Pydantic AI | LangGraph | smolagents | Difficulty |
| --- | --- | --- | --- | --- |
| q1: Services on prod-us-east-1 | 5 | 5 | 1 | easy |
| q2: Open critical vulns | 5 | 5 | 1 | easy |
| q3: Sev2→Sev1 escalation triggers | 5 | 5 | 1 | easy |
| q4: auth-service deploy compliance | 3 | 2 | 1 | coordination |
| q5: FW-404 authorization | 5 | 5 | 0 | coordination |
| q6: Vulns + ticketless deploys | 3 | 5 | 0 | coordination |
| q7: INC-4001 root cause + IR | 5 | 5 | 0 | coordination |
| q8: INC-4002 full analysis | **5** | **0** | 0 | hard_coordination |
| q9: INC-4002 remediation plan | 4 | 2 | 0 | coordination |
| q10: INC-4002 sev2→sev1 escalation | **5** | **0** | 0 | hard_coordination |

Key observations:
- **Easy questions (q1-q3)**: All frameworks that complete queries score 5/5. These require only a single specialist and single data source.
- **Coordination questions (q4-q7, q9)**: Pydantic AI and LangGraph both handle these, but LangGraph shows more variance (2-5/5) while Pydantic AI is more consistent (3-5/5).
- **Hard coordination (q8, q10)**: The biggest differentiator. These require all 3 specialists to gather and cross-reference evidence from infrastructure, security, and runbook domains. Pydantic AI scores 5/5 on both; LangGraph times out on both (0/5).

### Baseline Mode

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Correctness (1-5) | **3.6** | 3.2 | 1.4 |
| Avg Completeness (1-5) | **3.3** | 2.7 | 1.4 |
| Avg Faithfulness (1-5) | **4.9** | 4.8 | 2.1 |
| Avg Latency (s) | 31.95 | **28.97** | **14.59** |
| Total Tokens | 70,235 | 60,995 | 33,100 |
| Est. Cost (USD) | $0.069 | $0.064 | $0.032 |
| Hop Coverage | 87.2% | 68.2% | 13.3% |

In baseline mode, the shared tool budget is much tighter (3 calls per specialist instead of the expanded capability budget). Pydantic AI still leads but the gap is smaller. The constrained budget limits all frameworks' ability to gather cross-domain evidence.

### Capability vs Baseline Uplift (Pydantic AI)

| Metric | Baseline | Capability | Change |
| --- | --- | --- | --- |
| Avg Correctness | 3.6 | 4.5 | +25% |
| Avg Completeness | 3.3 | 4.1 | +24% |
| Hop Coverage | 87.2% | 85.8% | -2% |
| Agent Coverage | 93.3% | 100% | +7% |
| Avg Latency (s) | 31.95 | 95.60 | +199% |
| Est. Cost (USD) | $0.069 | $0.296 | +329% |

Capability mode delivers meaningfully better answer quality at the cost of ~3x latency and ~4x cost. The hop coverage stays roughly constant because capability mode already had good retrieval in baseline — the quality improvement comes from better evidence synthesis across specialists, not more retrieval.

## Model Comparison: GPT-5-mini vs Claude Haiku 4.5

We ran the multi-agent coordination scenario (capability mode) with Claude Haiku 4.5 to assess whether framework rankings are model-dependent. Claude Haiku 4.5 supports `temperature=0` and `stop` sequences, addressing both determinism and smolagents compatibility issues.

### Side-by-Side: Capability Mode Correctness

| Framework | GPT-5-mini | Claude Haiku 4.5 | Delta |
| --- | --- | --- | --- |
| **Pydantic AI** | 4.5/5 | **4.3/5** | -0.2 |
| **LangGraph** | 3.4/5 | 2.3/5 | -1.1 |
| **smolagents** | 0.4/5 | **2.1/5** | +1.7 |

### Full Metrics with Claude Haiku 4.5

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Correctness (1-5) | **4.3** | 2.3 | 2.1 |
| Avg Completeness (1-5) | **4.2** | 1.8 | 2.2 |
| Avg Faithfulness (1-5) | **4.0** | 2.8 | 1.7 |
| Avg Latency (s) | 30.3 | **18.8** | 105.9 |
| Total Tokens | 260,023 | 145,485 | 56,724 |
| Est. Cost (USD) | $0.34 | $0.15 | $0.07 |
| Agent Coverage | 100% | 58.3% | 100% |
| Hop Coverage | 91.7% | 26.7% | 30.0% |
| Coordination Success Rate | 57.1% | 0% | 0% |

### Key Observations

1. **Pydantic AI remains the clear leader across both models.** Its agent-as-tool pattern is model-agnostic — the coordinator delegates effectively regardless of which LLM is used. Correctness dropped only 0.2 points (4.5→4.3), while latency improved 3x (95.6s→30.3s) since Claude Haiku is a non-reasoning model with faster inference.

2. **LangGraph dropped significantly (3.4→2.3).** Claude Haiku appears less effective at LangGraph's routing pattern than GPT-5-mini. The router node, which must classify each query into the correct specialist category, likely benefits from GPT-5-mini's stronger reasoning capabilities. With Claude Haiku, the router under-delegates (58.3% agent coverage vs 68.3% with GPT-5-mini), and hop coverage collapsed from 66.7% to 26.7%.

3. **smolagents improved dramatically (0.4→2.1)** — confirming that the GPT-5-mini results were primarily a model compatibility issue, not an architectural limitation. With Claude Haiku supporting `stop` sequences, smolagents' step control works correctly — no timeouts, 100% agent coverage, and 100% tool coverage. However, it still hits max_steps on most coordination questions, suggesting the step budget needs tuning for this scenario.

4. **Latency improved across the board.** Claude Haiku is 2-7x faster than GPT-5-mini on this scenario because it doesn't perform extended "thinking" like GPT-5-mini's reasoning mode. Pydantic AI dropped from 95.6s to 30.3s, LangGraph from 137.3s to 18.8s.

5. **Framework rankings are partially model-dependent.** The top framework (Pydantic AI) is stable, but the gap between LangGraph and smolagents reversed: with GPT-5-mini, LangGraph was clearly second; with Claude Haiku, they're tied at ~2.2/5. This suggests that LangGraph's routing architecture benefits disproportionately from stronger reasoning models.

Usage: `uv run python scripts/run_eval.py --all --scenario multi_agent_coordination --mode capability --model claude-haiku-4-5-20251001`

## Previous Findings: Agentic SQL (Capability)

- Best overall balance in this scenario: **Pydantic AI**.
  - Strong quality (`correctness/completeness/faithfulness`) with lower latency/cost than alternatives.
  - Why it works well here: native tool loop stays efficient while still grounding decisions in SQL + docs.
- **LangGraph** is close on efficiency but less consistent on hard branching outcomes in this run.
  - Why: graph loop is robust, but additional iterations/tool turns can amplify variance on decision-heavy questions.
- **smolagents** remains the most expensive/slow path in this scenario configuration.
  - Why: smolagents relies on the `stop` parameter to control its agent step loop, but GPT-5-mini is a reasoning model that does not support stop sequences. This causes inefficient step usage, frequent `max_steps` exhaustion, and timeouts. This is a known framework-model incompatibility, not a reflection of smolagents' capability with compatible models (e.g. gpt-4o-mini).

## Model Determinism Note

GPT-5-mini (and all GPT-5 family reasoning models) do not support `temperature=0` or `stop` sequences. This means benchmark results are inherently non-deterministic — we observed individual question scores varying by up to 2 points between identical runs (e.g. q6 dropping from 5/5 to 3/5 purely due to LLM variance).

To address this, we added a `--runs N` flag to the evaluation harness. When N > 1, each framework is evaluated N times and results are averaged per-question, with standard deviations tracked. This provides honest, variance-aware benchmarking. Individual run results are saved alongside the aggregated result for auditability.

Usage: `uv run python scripts/run_eval.py --all --scenario multi_agent_coordination --mode capability --runs 3`

## Artifacts

### Multi-Agent Coordination (Claude Haiku 4.5)
- Pydantic AI: [`results/pydantic_ai_multi_agent_coordination_20260212_172010.json`](results/pydantic_ai_multi_agent_coordination_20260212_172010.json)
- LangGraph: [`results/langgraph_multi_agent_coordination_20260212_172501.json`](results/langgraph_multi_agent_coordination_20260212_172501.json)
- smolagents: [`results/smolagents_multi_agent_coordination_20260212_174349.json`](results/smolagents_multi_agent_coordination_20260212_174349.json)

### Multi-Agent Coordination (GPT-5-mini)
- Pydantic AI capability: [`results/pydantic_ai_multi_agent_coordination_20260212_143505.json`](results/pydantic_ai_multi_agent_coordination_20260212_143505.json)
- LangGraph capability: [`results/langgraph_multi_agent_coordination_20260212_144640.json`](results/langgraph_multi_agent_coordination_20260212_144640.json)
- smolagents capability: [`results/smolagents_multi_agent_coordination_20260212_145443.json`](results/smolagents_multi_agent_coordination_20260212_145443.json)
- Pydantic AI baseline: [`results/pydantic_ai_multi_agent_coordination_20260212_132134.json`](results/pydantic_ai_multi_agent_coordination_20260212_132134.json)
- LangGraph baseline: [`results/langgraph_multi_agent_coordination_20260212_132654.json`](results/langgraph_multi_agent_coordination_20260212_132654.json)
- smolagents baseline: [`results/smolagents_multi_agent_coordination_20260212_133216.json`](results/smolagents_multi_agent_coordination_20260212_133216.json)

### Agentic SQL
- Pydantic AI: [`results/pydantic_ai_agentic_sql_qa_20260211_174017.json`](results/pydantic_ai_agentic_sql_qa_20260211_174017.json)
- LangGraph: [`results/langgraph_agentic_sql_qa_20260211_174355.json`](results/langgraph_agentic_sql_qa_20260211_174355.json)
- smolagents: [`results/smolagents_agentic_sql_qa_20260211_171939.json`](results/smolagents_agentic_sql_qa_20260211_171939.json)
