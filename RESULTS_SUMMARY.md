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
- **Stop sequence dependency is a critical compatibility axis.** Frameworks that use text-based ReAct loops (CrewAI, smolagents) depend on stop sequences to control agent iterations. Reasoning models (GPT-5-mini, o3, o4-mini) do not support stop sequences, causing agent loop failures, token blowup, and raw internal state leaking into final answers. Frameworks using native function-calling APIs (Pydantic AI, LangGraph) are unaffected. As the industry shifts toward reasoning models, this becomes a key framework selection criterion.

## Why Frameworks Differ

### On Multi-hop QA

- **Pydantic AI**: structured planner + sufficiency-check loop improves recall with controlled behavior. Can still miss difficult bridge mappings (e.g. rack-to-datacenter edge cases).
- **LangGraph**: explicit graph loop (`retrieve -> assess -> retrieve/generate`) is robust for iterative evidence gathering. Extra graph iterations can inflate token and latency budgets.
- **smolagents**: tool-driven agent loop is very good at deep multi-step exploration and often reaches highest chain coverage. Highest orchestration overhead (more tokens/time) due to GPT-5-mini not supporting the `stop` parameter.
- **CrewAI**: planner + checker + answer agents in sequential Crew runs achieve 83.3% chain success (highest) and 88.9% hop coverage. But token usage is extremely high ($1.91 for 9 questions) because each Crew run carries heavy internal system prompts.

### On Agentic SQL QA

- **LangGraph** (5.0/5): perfect correctness with efficient graph-based tool loop. Lowest cost at $0.027.
- **CrewAI** (5.0/5): ties LangGraph on correctness. Tool-calling via `BaseTool` works well for SQL queries. 2x slower and 2x more expensive than LangGraph due to ReAct overhead.
- **Pydantic AI** (4.8/5): near-perfect with native function calling. Clean, minimal implementation.
- **smolagents** (2.5/5): stop sequence issues cause half the branching questions to fail.

### On Multi-Agent Coordination

- **Pydantic AI** (4.5/5 capability correctness)
  - Strength: agent-as-tool pattern lets the coordinator call specialist sub-agents as functions. Each specialist runs with its own prompt and tool access, then returns structured results to the coordinator. This cleanly separates domain concerns and allows the coordinator to synthesize evidence from multiple specialists.
  - Result: 100% agent coverage, 100% tool coverage, 85.8% hop coverage. Scored 5/5 on all 3 easy questions and 4-5/5 on most coordination questions.
- **LangGraph** (3.4/5 capability correctness)
  - Strength: supervisor graph with conditional routing can delegate to specialist nodes. Graph structure is explicit and auditable.
  - Limitation: with the default 5-minute query timeout, the hardest coordination questions (q8, q10) timed out at 300s. The supervisor sometimes under-delegates, using only 1-2 specialists when 3 are needed, resulting in 68.3% agent coverage. Scored 5/5 on easy questions but dropped to 0-2/5 on hard coordination.
- **CrewAI** (0.2/5 capability correctness)
  - Approach: `Process.hierarchical` with coordinator as `manager_agent` and 3 specialist agents (infrastructure, security, runbook). CrewAI handles delegation automatically through the hierarchical process.
  - Limitation: GPT-5-mini does not support stop sequences, and CrewAI's ReAct loop relies on `\nObservation:` as a stop token. The model generates past this boundary, fabricating fake tool observations. In capability mode, 9 out of 10 questions timed out at 300s — the hierarchical process overhead combined with stop sequence incompatibility made multi-agent delegation prohibitively slow. Token usage was 2.5M (10x more than Pydantic AI) at $3.06 cost. See [Reasoning Models and Stop Sequence Compatibility](#reasoning-models-and-stop-sequence-compatibility) for details.
- **smolagents** (0.4/5 capability correctness)
  - Limitation: fundamentally broken on this scenario with GPT-5-mini. The `stop` parameter incompatibility causes step control failures, and OpenAI 500 errors on long queries compound the problem. 8 out of 10 questions timed out or errored. This is a framework-model incompatibility, not a reflection of smolagents' architecture.

## Scenario-level Interpretation

- For **simple RAG QA**, all frameworks can be effective with low complexity.
- For **multi-hop QA**, framework orchestration style matters more than single-pass retrieval quality.
- For **agentic SQL QA**, tool loop efficiency and error handling determine success.
- For **multi-agent coordination**, the ability to delegate to and synthesize from multiple specialist agents is the primary differentiator. This is where framework architecture matters most.
- If your priority is best answer quality under loose budgets, the most agentic approach can win.
- If your priority is predictable cost/latency, structured or graph-based loops are generally easier to control.
- If you plan to use **reasoning models** (GPT-5-mini, o3, o4-mini), prefer frameworks that use native function-calling APIs (Pydantic AI, LangGraph) over those relying on stop-sequence-controlled ReAct loops (CrewAI, smolagents).

## Latest Findings: Multi-Agent Coordination

### Capability Mode

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Correctness (1-5) | **4.9** | 3.6 | 1.0 | 0.2 |
| Avg Completeness (1-5) | **4.4** | 3.6 | 1.0 | 0.2 |
| Avg Faithfulness (1-5) | **4.9** | 3.9 | 1.0 | 0.2 |
| Avg Latency (s) | **77.3** | 125.1 | 156.0 | 284.8 |
| Total Tokens | 322,081 | 942,719 | 0 | 2,516,016 |
| Est. Cost (USD) | $0.28 | $0.39 | $0.00 | $3.06 |
| Hop Coverage | 92.5% | 72.5% | 0% | 6.7% |
| Agent Coverage | 95.0% | 83.3% | 80.0% | 5.0% |
| Coordination Success Rate | 71.4% | 71.4% | 0% | 0% |

Key observations:
- **Pydantic AI dominates** with 4.9/5 correctness, 95% agent coverage, and 71.4% coordination success.
- **LangGraph** is a solid second at 3.6/5, with improved coordination success (71.4%) compared to earlier runs.
- **smolagents and CrewAI** both struggle fundamentally with GPT-5-mini due to stop sequence incompatibility. CrewAI's hierarchical process adds delegation overhead that compounds the issue, making it the slowest and most expensive framework on this scenario ($3.06 for 10 questions).

### Baseline Mode

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Correctness (1-5) | **3.7** | 3.6 | 1.4 | 2.6 |
| Avg Completeness (1-5) | **3.3** | 3.4 | 1.4 | 2.2 |
| Avg Faithfulness (1-5) | **4.7** | 4.8 | 1.3 | 3.1 |
| Avg Latency (s) | 31.08 | 31.26 | **10.64** | 69.79 |
| Total Tokens | 62,582 | 71,164 | 28,742 | 519,170 |
| Est. Cost (USD) | $0.071 | $0.073 | $0.025 | $0.611 |
| Hop Coverage | 76.8% | 85.7% | 13.3% | 47.5% |

In baseline mode (single agent with all 3 tools), Pydantic AI and LangGraph are near-parity. CrewAI places third at 2.6/5 — its single-agent baseline works better than its hierarchical capability mode because there's no delegation overhead, but token usage is still 8x higher than Pydantic AI due to CrewAI's verbose internal prompts.

### Capability vs Baseline Uplift (Pydantic AI)

| Metric | Baseline | Capability | Change |
| --- | --- | --- | --- |
| Avg Correctness | 3.7 | 4.9 | +32% |
| Avg Completeness | 3.3 | 4.4 | +33% |
| Hop Coverage | 76.8% | 92.5% | +20% |
| Agent Coverage | 78.3% | 95.0% | +21% |
| Avg Latency (s) | 31.08 | 77.27 | +149% |
| Est. Cost (USD) | $0.071 | $0.285 | +301% |

Capability mode delivers meaningfully better answer quality at the cost of ~2.5x latency and ~4x cost. Both hop coverage and agent coverage improve significantly, showing that dedicated specialist agents with expanded budgets find more evidence than a single agent with tight constraints.

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

## All-Scenario Summary (GPT-5-mini)

| Scenario | Mode | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- | --- |
| RAG QA | baseline | 4.4/5 | 4.4/5 | 4.4/5 | 4.4/5 |
| Multihop QA | capability | 3.8/5 | 4.1/5 | 3.3/5 | 3.8/5 |
| Agentic SQL | capability | 4.8/5 | **5.0/5** | 2.5/5 | **5.0/5** |
| Multi-Agent Coord | capability | **4.9/5** | 3.6/5 | 1.0/5 | 0.2/5 |
| Multi-Agent Coord | baseline | **3.7/5** | 3.6/5 | 1.4/5 | 2.6/5 |

Key takeaways:
- **RAG QA**: All frameworks achieve parity at 4.4/5. The task is simple enough that framework choice doesn't matter.
- **Multihop QA**: LangGraph leads slightly at 4.1/5. CrewAI matches Pydantic AI at 3.8/5 but at 26x the cost ($1.91 vs $0.07).
- **Agentic SQL**: LangGraph and CrewAI both achieve perfect 5.0/5. CrewAI's tool-calling works very well for single-agent tool use.
- **Multi-Agent Coordination**: The most differentiating scenario. Pydantic AI dominates at 4.9/5. CrewAI collapses to 0.2/5 in capability mode due to hierarchical process overhead + stop sequence issues.
- **CrewAI excels at single-agent tool use but struggles with multi-agent delegation.** Its strength is agentic SQL (5.0/5); its weakness is multi-agent coordination with reasoning models.

## Previous Findings: Agentic SQL (Capability)

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Correctness (1-5) | 4.8 | **5.0** | 2.5 | **5.0** |
| Avg Completeness (1-5) | 4.6 | **5.0** | 2.5 | 4.6 |
| Avg Faithfulness (1-5) | **5.0** | **5.0** | 2.5 | 4.8 |
| Avg Latency (s) | 14.6 | **12.5** | 95.6 | 27.9 |
| Total Tokens | 83,930 | 68,735 | 121,188 | 82,740 |
| Est. Cost (USD) | $0.034 | **$0.027** | $0.076 | $0.058 |
| Tool Coverage | 93.8% | **100%** | 50.0% | **100%** |

- **LangGraph** achieves perfect 5.0/5 with lowest cost — the graph-based tool loop is ideal for SQL query scenarios.
- **CrewAI** ties LangGraph on correctness (5.0/5) with 100% tool coverage. This is CrewAI's strongest scenario — single-agent tool calling via `BaseTool` works well even with reasoning models. The ReAct loop overhead is manageable when only 1 agent is needed.
- **Pydantic AI** scores 4.8/5 with the most efficient token usage among top performers.
- **smolagents** struggles at 2.5/5 due to stop sequence incompatibility causing half the branching questions to fail.

## Reasoning Models and Stop Sequence Compatibility

GPT-5-mini (and all GPT-5 family reasoning models) do not support `temperature=0` or `stop` sequences. This has two distinct effects on benchmark results:

### 1. Non-deterministic outputs

Without `temperature=0`, results vary between identical runs — we observed individual question scores fluctuating by up to 2 points (e.g. q6 dropping from 5/5 to 3/5 purely due to LLM variance). To address this, we added a `--runs N` flag. When N > 1, each framework is evaluated N times and results are averaged per-question, with standard deviations tracked.

Usage: `uv run python scripts/run_eval.py --all --scenario multi_agent_coordination --mode capability --runs 3`

### 2. Agent loop control failures (stop sequence dependency)

Several frameworks rely on stop sequences to control their internal agent loops. The most common pattern is **ReAct** (Thought → Action → Observation), where the framework sets `stop=["\nObservation:"]` so the model halts after outputting `Action Input: {...}`, allowing the framework to execute the real tool and inject results. Without stop sequence support, the model generates past the boundary, fabricating fake tool outputs in a single response.

**Affected frameworks:**

| Framework | Internal loop | Stop dependency | Effect with GPT-5-mini |
| --- | --- | --- | --- |
| **CrewAI** | ReAct (Thought/Action/Observation) | `\nObservation:` stop token | Model generates past the Action boundary, fabricating observations. Hits `max_iter` with raw Thought/Action blocks as final output instead of synthesized answers. Token usage inflated 5-10x. |
| **smolagents** | Step-based with `stop` parameter | Framework-level stop sequences | Step control fails entirely. Agent exhausts `max_steps` budget and times out. 8/10 questions failed in multi-agent coordination. |
| **Pydantic AI** | Native function calling (no ReAct) | None — uses API-level tool calls | Unaffected. The model uses structured tool-call API, not text-based stop sequences. |
| **LangGraph** | Graph nodes with function calling | None — uses API-level tool calls | Unaffected. Routing and tool calls use the OpenAI function-calling API. |

This is a critical finding for production deployments: **as the industry shifts toward reasoning models (GPT-5-mini, o3, o4-mini), frameworks that depend on stop sequences for agent loop control will face increasing compatibility issues.** Frameworks using native function-calling APIs (Pydantic AI, LangGraph) are inherently more resilient to this shift.

#### Evidence: CrewAI Thought/Action leakage

In CrewAI's multi-agent coordination results, 4 out of 10 questions returned raw agent internal state instead of answers:

| Question | Returned output | Score |
| --- | --- | --- |
| Q2: Open critical vulns | `Thought: I should retrieve... Action: query_infrastructure Action Input: {...}` | 1/5 |
| Q4: auth-service compliance | `Thought: I need the change management... Action: lookup_runbook Action Input: {...}` | 1/5 |
| Q6: Vulns + ticketless deploys | `Thought: I should fetch recent_deploys... Action: query_infrastructure Action Input: {...}` | 1/5 |
| Q7: INC-4001 root cause | `Thought: Query security logs... Action: query_security Action Input: {...}` | 1/5 |

These are all coordination questions requiring 3+ tool calls. The agent exhausted its `max_iter` budget while generating fabricated Thought/Action cycles (because the `\nObservation:` stop token was ignored), and CrewAI returned the last buffer contents — a mid-loop planning block rather than a synthesized answer.

This bug is tracked as [crewAIInc/crewAI#3836](https://github.com/crewAIInc/crewAI/issues/3836) (originally reported for Anthropic models, but the same pattern affects any model that doesn't honor stop sequences).

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
- Pydantic AI: [`results/pydantic_ai_agentic_sql_qa_20260212_223622.json`](results/pydantic_ai_agentic_sql_qa_20260212_223622.json)
- LangGraph: [`results/langgraph_agentic_sql_qa_20260212_223832.json`](results/langgraph_agentic_sql_qa_20260212_223832.json)
- smolagents: [`results/smolagents_agentic_sql_qa_20260212_225131.json`](results/smolagents_agentic_sql_qa_20260212_225131.json)
- CrewAI: [`results/crewai_agentic_sql_qa_20260212_225547.json`](results/crewai_agentic_sql_qa_20260212_225547.json)

### RAG QA
- Pydantic AI: [`results/pydantic_ai_rag_qa_20260212_220633.json`](results/pydantic_ai_rag_qa_20260212_220633.json)
- LangGraph: [`results/langgraph_rag_qa_20260212_220739.json`](results/langgraph_rag_qa_20260212_220739.json)
- smolagents: [`results/smolagents_rag_qa_20260212_220847.json`](results/smolagents_rag_qa_20260212_220847.json)
- CrewAI: [`results/crewai_rag_qa_20260212_221025.json`](results/crewai_rag_qa_20260212_221025.json)

### Multihop QA
- Pydantic AI: [`results/pydantic_ai_multihop_qa_20260212_224045.json`](results/pydantic_ai_multihop_qa_20260212_224045.json)
- LangGraph: [`results/langgraph_multihop_qa_20260212_224456.json`](results/langgraph_multihop_qa_20260212_224456.json)
- smolagents: [`results/smolagents_multihop_qa_20260212_230221.json`](results/smolagents_multihop_qa_20260212_230221.json)
- CrewAI: [`results/crewai_multihop_qa_20260212_231148.json`](results/crewai_multihop_qa_20260212_231148.json)
