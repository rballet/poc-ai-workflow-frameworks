# Framework Comparison Report

Generated: 2026-02-11 21:39 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: capability
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 17.91 | 16.72 | 112.47 |
| Total Tokens | 71,045 | 74,547 | 45,895 |
| Est. Cost (USD) | $0.0281 | $0.0274 | $0.0299 |
| Avg Correctness (1-5) | 5.0 | 4.8 | 1.2 |
| Avg Completeness (1-5) | 4.9 | 4.5 | 1.2 |
| Avg Faithfulness (1-5) | 5.0 | 4.8 | 1.2 |
| Avg Retrieval Precision | 0.85 | 0.85 | 0.15 |
| Avg Retrieval Recall | 0.96 | 0.91 | 0.25 |

> **Note on smolagents performance:** smolagents relies on the `stop` parameter
> to control its agent step loop. OpenAI's GPT-5 family (including gpt-5-mini)
> are reasoning models that [do not support `stop` sequences](https://community.openai.com/t/why-doesnt-gpt-5-1-support-stop-sequences/1366800).
> This causes smolagents to use steps less efficiently, leading to frequent
> `max_steps` exhaustion, timeouts, and degraded answer quality. This is a known
> framework-model incompatibility ([smolagents #1893](https://github.com/huggingface/smolagents/issues/1893)),
> not a reflection of smolagents' capability with compatible models (e.g. gpt-4o-mini).

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Capability | 68.5 | 54.6 | 6.2 |
| Efficiency | 23.6 | 26.7 | 6.7 |
| Developer Experience | 92.8 | 40.2 | 78.7 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency p50 (s) | 17.25 | 14.40 | 120.00 |
| Latency p95 (s) | 30.28 | 32.33 | 120.00 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Branching Avg Grounded Hop Coverage | 0.750 | 0.500 | 0 |
| Branching Avg Hop Coverage | 0.750 | 0.500 | 0 |
| Branching Avg Tool Coverage | 0.875 | 0.875 | 0 |
| Branching Questions | 4 | 4 | 4 |
| Branching Success Avg | 0.125 | 0.125 | 0 |
| Branching Success Rate | 0.250 | 0.250 | 0 |
| Easy Avg Hop Coverage | 1 | 1 | 0.500 |
| Easy Questions | 4 | 4 | 4 |
| Grounded Hop Coverage Avg | 0.875 | 0.750 | 0.250 |
| Has Tool Trace Avg | 1 | 1 | 0.250 |
| Hop Coverage Avg | 0.875 | 0.750 | 0.250 |
| Is Branching Avg | 0.500 | 0.500 | 0.500 |
| Is Easy Avg | 0.500 | 0.500 | 0.500 |
| Matched Hops Avg | 1.625 | 1.250 | 0.250 |
| Matched Tools Avg | 1.375 | 1.375 | 0.250 |
| Required Hops Avg | 2 | 2 | 2 |
| Required Tools Avg | 1.500 | 1.500 | 1.500 |
| Tool Calls Reported Avg | 5.875 | 6.125 | 1.250 |
| Tool Coverage Avg | 0.938 | 0.938 | 0.250 |
| Tool Trace Rate | 1 | 1 | 0.250 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Source Lines (SLOC) | 132 | 177 | 169 |
| Comment Ratio | 0% | 0% | 0% |
| Avg Cyclomatic Complexity | 2.2 | 3.3 | 2.4 |
| Max Cyclomatic Complexity | 6 | 10 | 8 |
| Complexity Grade | A | A | A |
| Maintainability Index | 40.0 | 32.8 | 36.6 |
| Maintainability Grade | A | A | A |
| Halstead Volume | 175 | 247 | 204 |
| Halstead Difficulty | 3.8 | 5.5 | 5.3 |
| Halstead Bugs (est.) | 0.06 | 0.08 | 0.07 |
| Total Imports | 8 | 11 | 9 |
| Framework Imports | 1 | 5 | 1 |
| Classes | 2 | 1 | 3 |
| Functions | 9 | 12 | 10 |
| Type Annotation Coverage | 100% | 92% | 100% |

## Code Quality — LLM Code Review

| Criterion | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Readability | 4 | 4 | 5 |
| Idiomatic Usage | 4 | 4 | 4 |
| Error Handling | 3 | 2 | 3 |
| Extensibility | 4 | 4 | 4 |
| Testability | 3 | 3 | 3 |
| Documentation | 3 | 3 | 4 |
| Abstraction | 4 | 4 | 4 |
| **Average** | 3.6 | 3.4 | 3.9 |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 8.52 | 6.51 | 94.56 |
| Tokens | 2,977 | 2,856 | 24,071 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 |
| Tool Calls Reported | 4 | 4 | 3 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Acme Health is on the "Enterprise" account tier and operates in the "us-west" region (from the customers table).
- **LangGraph**: Acme Health is an Enterprise-tier account operating in the us-west region.
- **smolagents**: Acme Health is in the “Enterprise” account tier and operates in the “us-west” region.

Evidence: customers table row for customer_id = C003 (name = 'Acme Health') returned tier = 'Enterprise' and region = 'us-west' (query: SELECT customer_id, name, tier, region, owner_team FROM customers WHERE name ...

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 7.31 | 7.53 | 120.00 |
| Tokens | 1,415 | 1,330 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 5 | 5 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 |
| Is Branching | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 1 | 1 | 0 |
| Required Hops | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 |
| Tool Calls Reported | 1 | 1 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: No. Per the Shipping Credit Policy, delay reasons that are weather (as well as customs hold or force majeure) are explicitly excluded from shipping-credit eligibility. The policy requires a delivered status plus a delivery delay of 24+ hours and a delay reason that is not weather. (support_policies....
- **LangGraph**: No. Per the Shipping Credit Policy: an order is eligible for a shipping credit only if (1) status is delivered, (2) delivery delay is 24 hours or more, and (3) delay reason is not weather, customs hold, or force majeure. (support_policies.md)
- **smolagents**: Query timed out before producing an answer.

### q3: How many unresolved P1 incidents are currently open?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 14.66 | 4.95 | 120.00 |
| Tokens | 3,536 | 2,423 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 5 | 5 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 1.00 | 1.00 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 |
| Is Branching | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 1 | 1 | 0 |
| Required Hops | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: There are 2 unresolved P1 incidents currently open.

Query used: SELECT COUNT(*) AS open_p1 FROM incidents WHERE severity = 'P1' AND resolved_at IS NULL; Result: open_p1 = 2.
- **LangGraph**: There are 2 unresolved P1 incidents currently open (severity = "P1" and resolved_at IS NULL).
- **smolagents**: Query timed out before producing an answer.

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 19.83 | 21.27 | 120.00 |
| Tokens | 11,205 | 13,141 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 5 | 5 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 0.80 | 0.80 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.667 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.667 | 0.667 | 0 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 0 |
| Matched Tools | 2 | 2 | 0 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 7 | 9 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Yes — ORD-104 is eligible for a shipping credit. Evidence:
- orders: ORD-104 status = "delivered" and total_usd = 7000.0.
- shipments: ORD-104 delay_hours = 30 and delay_reason = "carrier_misroute".
- customers: C003 (order's customer) tier = "Enterprise".
- policy (Shipping Credit Policy): eligibil...
- **LangGraph**: Yes — ORD-104 is eligible for a shipping credit.

Evidence:
- orders row: status = "delivered", total_usd = 7000.00 (orders table).
- shipments row: delay_hours = 30, delay_reason = "carrier_misroute" (shipments table). 30 ≥ 24 and carrier_misroute is not an excluded reason.
- customer row: tier = "...
- **smolagents**: Query timed out before producing an answer.

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 28.42 | 34.20 | 120.00 |
| Tokens | 17,544 | 16,514 | 0 |
| Correctness | 5 | 3 | 0 |
| Completeness | 5 | 2 | 0 |
| Faithfulness | 5 | 4 | 0 |
| Retrieval Prec | 0.83 | 0.80 | 0.00 |
| Retrieval Recall | 1.00 | 0.80 | 0.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.667 | 0 | 0 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 0 | 0 |
| Matched Tools | 2 | 2 | 0 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 9 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Yes — CASE-778 should be auto‑escalated.

Why (evidence):
- CASE-778 is high priority, customer_waiting_hours = 26 (>24), and last_update_hours = 7 (>6) (support_cases table) — these meet the auto‑escalation triggers for Enterprise waiting >24h and high‑priority with no agent update >6h.
- There is ...
- **LangGraph**: Yes — CASE-778 should be auto‑escalated.

Why (evidence):
- Case data (support_cases): CASE-778 is priority = "high", customer_waiting_hours = 26, last_update_hours = 7. (support_cases table)
- Customer data (customers): customer_id C003 (case owner) is tier = "Enterprise" and owner_team = "Strategi...
- **smolagents**: Query timed out before producing an answer.

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 26.42 | 24.60 | 120.00 |
| Tokens | 14,490 | 19,555 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 5 | 5 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 0.67 | 0.67 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Branching Success | 1 | 1 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 |
| Matched Tools | 2 | 2 | 0 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 9 | 10 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Offer a goodwill credit of 8% of the order total = $760 to the customer.

Evidence and logic:
- Order ORD-109: status = delivered, total_usd = $9,500 (orders table).
- Shipment: delay_hours = 12 (shipments table) — below the 24‑hour threshold for shipping credits.
- Incident: category = pick_pack_er...
- **LangGraph**: Offer a goodwill credit of $760 to the customer.

Rationale / evidence:
- Policy: for pick_pack_error on delivered orders, offer a goodwill credit; Enterprise customers receive 8% of order total. (support_policies.md)
- Order ORD-109: status = delivered, total_usd = $9,500. (orders table)
- Customer...
- **smolagents**: Query timed out before producing an answer.

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 6.82 | 5.85 | 85.22 |
| Tokens | 2,321 | 2,290 | 21,824 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 4 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 0.20 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 7 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: The on-call primary for the Commercial team is Omar Santos. The on-call secondary is Lina Hoffmann. (Source: oncall table query.)
- **LangGraph**: Primary on-call engineer for the Commercial team: Omar Santos.
Secondary (backup): Lina Hoffmann.
- **smolagents**: The current on-call engineer for the Commercial team is Omar Santos (primary engineer). Source: oncall table row — team: Commercial; primary_engineer: Omar Santos; secondary_engineer: Lina Hoffmann.

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 31.27 | 28.85 | 120.00 |
| Tokens | 17,557 | 16,438 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 4 | 4 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 1.00 | 1.00 | 0.00 |
| Retrieval Recall | 0.67 | 0.50 | 0.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.333 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.667 | 0.333 | 0 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 1 | 0 |
| Matched Tools | 1 | 1 | 0 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 10 | 0 |
| Tool Coverage | 0.500 | 0.500 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: Keep it with account support — do not wake the Sev1 commander now.

Grounding from the data:
- incidents: INC-9003 for order ORD-109 has severity = "P2" and resolved_at = "2026-02-08T12:30:00Z" (i.e., it was not a P1/Sev1 and is marked resolved).  
- customers: Northwind Hospitals is E...
- **LangGraph**: Findings from our records:
- Order ORD-109 has one incident (INC-9003) with severity = P2. It was opened 2026-02-08T11:00:00Z and shows resolved_at = 2026-02-08T12:30:00Z.
- Customer for ORD-109 is Northwind Hospitals (customer_id C001, tier = Enterprise).
- There is no support_cases row with case_i...
- **smolagents**: Query timed out before producing an answer.
