# Framework Comparison Report

Generated: 2026-02-11 18:02 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: capability
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 21.11 | 23.59 | 232.01 |
| Total Tokens | 68,007 | 75,505 | 544,999 |
| Est. Cost (USD) | $0.0276 | $0.0298 | $0.3178 |
| Avg Correctness (1-5) | 4.8 | 4.5 | 4.5 |
| Avg Completeness (1-5) | 4.9 | 4.4 | 4.4 |
| Avg Faithfulness (1-5) | 5.0 | 4.8 | 5.0 |
| Avg Retrieval Precision | 0.84 | 0.86 | 0.80 |
| Avg Retrieval Recall | 0.93 | 0.95 | 0.98 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Capability | 84.8 | 60.2 | 75.2 |
| Efficiency | 33.3 | 33.0 | 0.0 |
| Developer Experience | 96.5 | 44.5 | 89.9 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency p50 (s) | 16.37 | 15.00 | 179.59 |
| Latency p95 (s) | 39.45 | 55.62 | 433.47 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Branching Avg Grounded Hop Coverage | 0.750 | 0.583 | 0.750 |
| Branching Avg Hop Coverage | 0.917 | 0.667 | 0.833 |
| Branching Avg Tool Coverage | 1 | 1 | 1 |
| Branching Questions | 4 | 4 | 4 |
| Branching Success Avg | 0.375 | 0.125 | 0.250 |
| Branching Success Rate | 0.750 | 0.250 | 0.500 |
| Easy Avg Hop Coverage | 1 | 1 | 1 |
| Easy Questions | 4 | 4 | 4 |
| Grounded Hop Coverage Avg | 0.875 | 0.792 | 0.875 |
| Has Tool Trace Avg | 1 | 1 | 1 |
| Hop Coverage Avg | 0.958 | 0.833 | 0.917 |
| Is Branching Avg | 0.500 | 0.500 | 0.500 |
| Is Easy Avg | 0.500 | 0.500 | 0.500 |
| Matched Hops Avg | 1.875 | 1.500 | 1.750 |
| Matched Tools Avg | 1.500 | 1.500 | 1.500 |
| Required Hops Avg | 2 | 2 | 2 |
| Required Tools Avg | 1.500 | 1.500 | 1.500 |
| Tool Calls Reported Avg | 5.750 | 6 | 5.875 |
| Tool Coverage Avg | 1 | 1 | 1 |
| Tool Trace Rate | 1 | 1 | 1 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Source Lines (SLOC) | 131 | 174 | 160 |
| Comment Ratio | 0% | 0% | 0% |
| Avg Cyclomatic Complexity | 2.2 | 3.2 | 2.2 |
| Max Cyclomatic Complexity | 6 | 10 | 8 |
| Complexity Grade | A | A | A |
| Maintainability Index | 40.3 | 33.5 | 38.6 |
| Maintainability Grade | A | A | A |
| Halstead Volume | 175 | 226 | 141 |
| Halstead Difficulty | 3.8 | 5.0 | 4.4 |
| Halstead Bugs (est.) | 0.06 | 0.08 | 0.05 |
| Total Imports | 8 | 11 | 9 |
| Framework Imports | 1 | 5 | 1 |
| Classes | 2 | 1 | 3 |
| Functions | 9 | 12 | 10 |
| Type Annotation Coverage | 100% | 92% | 100% |

## Code Quality — LLM Code Review

| Criterion | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Readability | 4 | 4 | 4 |
| Idiomatic Usage | 5 | 5 | 5 |
| Error Handling | 4 | 4 | 4 |
| Extensibility | 4 | 4 | 4 |
| Testability | 4 | 4 | 4 |
| Documentation | 4 | 4 | 4 |
| Abstraction | 5 | 5 | 5 |
| **Average** | 4.3 | 4.3 | 4.3 |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 7.15 | 6.98 | 77.31 |
| Tokens | 2,462 | 2,857 | 20,329 |
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
| Tool Calls Reported | 3 | 4 | 3 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Acme Health is on the Enterprise tier and operates in the us-west region (customer_id C003).
- **LangGraph**: Acme Health is on the Enterprise tier and its operating region is us-west.
- **smolagents**: Acme Health is on the Enterprise account tier and operates in the us-west region (customers table — customer_id C003).

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 9.30 | 6.66 | 184.66 |
| Tokens | 1,381 | 1,298 | 50,579 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 4 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
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
| Tool Calls Reported | 1 | 1 | 5 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: No. Per the Shipping Credit Policy, weather-related delays are explicitly excluded from shipping credits.

Relevant policy points (support_policies.md):
- An order is eligible for a shipping credit only when all are true: status = delivered; delivery delay ≥ 24 hours; delay reason is NOT weather, cu...
- **LangGraph**: No. Per the Shipping Credit Policy, weather-related delays are excluded.

Eligibility requires all of the following:
- Order status = delivered
- Delivery delay ≥ 24 hours
- Delay reason is NOT weather, customs hold, or force majeure

(For reference, the policy also lists credit caps by account tier...
- **smolagents**: Short answer: No — weather-related shipment delays are not eligible for shipping credits.

Grounding (policy): The Shipping Credit Policy states: “An order is eligible for a shipping credit when all of the following are true: 1. Status is `delivered`. 2. Delivery delay is 24 hours or more. 3. Delay ...

### q3: How many unresolved P1 incidents are currently open?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 10.47 | 7.66 | 113.75 |
| Tokens | 3,522 | 2,465 | 25,995 |
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
| Tool Calls Reported | 3 | 3 | 3 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: There are 2 unresolved P1 incidents (severity = 'P1' and resolved_at IS NULL).
- **LangGraph**: There are 2 unresolved P1 incidents currently open.
- **smolagents**: There are 2 unresolved P1 incidents currently open.

Query used: SELECT COUNT(*) AS unresolved_p1_count FROM incidents WHERE severity = 'P1' AND resolved_at IS NULL;
Definition used: an incident is considered unresolved/open if incidents.resolved_at IS NULL.

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 22.28 | 22.34 | 174.53 |
| Tokens | 12,609 | 11,696 | 50,453 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.80 | 0.80 | 0.80 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.667 | 0.667 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0.667 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 2 |
| Matched Tools | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 9 | 8 | 5 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Yes. ORD-104 is eligible for a shipping credit.

Evidence:
- Order ORD-104: status = "delivered", total_usd = 7000.00 (orders table).
- Shipment ORD-104: delay_hours = 30, delay_reason = "carrier_misroute" (shipments table). Delay >= 24 and reason is not excluded.
- Customer C003 (owner of ORD-104) ...
- **LangGraph**: Yes.

Evidence:
- Order ORD-104 status = delivered (orders table).
- Delivery delay = 30 hours and delay_reason = carrier_misroute (shipments table).
- Shipping-credit eligibility requires: delivered, delay ≥ 24 hours, and reason not weather/customs/force majeure — carrier_misroute is allowed (suppo...
- **smolagents**: Yes — ORD-104 is eligible for a shipping credit. Evidence and calculation:

Evidence from database and policy:
- orders row (ORD-104): status = delivered; total_usd = 7000.00.
- shipments row (ORD-104): delay_hours = 30; delay_reason = carrier_misroute (delivered_at present).
- customers row (C003):...

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 37.04 | 55.21 | 392.65 |
| Tokens | 17,926 | 19,443 | 120,320 |
| Correctness | 3 | 5 | 5 |
| Completeness | 4 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.75 | 0.83 | 0.71 |
| Retrieval Recall | 0.60 | 1.00 | 1.00 |
| Branching Success | 1 | 1 | 1 |
| Grounded Hop Coverage | 0.667 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 3 |
| Matched Tools | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 10 | 9 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer
- I cannot definitively say whether CASE-778 should have been auto‑escalated because I do not have the auto‑escalation policy/criteria in the available data.
- Based on the case/incident data, I recommend technical ownership be assigned to Platform Reliability and customer/relationship ...
- **LangGraph**: Short answer
- Yes — CASE-778 should be auto‑escalated immediately.
- Owning team: Platform Reliability (page the Platform Reliability on‑call: Nikhil Batra).

Why (evidence from the database + policy documents)
- The order for this case (ORD-102) has an active unresolved P1 incident (INC-9001, seve...
- **smolagents**: Decision: Yes — CASE-778 should be auto‑escalated immediately.

Grounding (evidence):
- support_cases CASE-778: priority = high; customer_waiting_hours = 26 (>24); last_update_hours = 7 (>6); status = open. (support_cases table)
- customers C003: tier = Enterprise; owner_team = Strategic Accounts. (...

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 32.41 | 27.25 | 356.51 |
| Tokens | 11,580 | 20,621 | 112,511 |
| Correctness | 5 | 1 | 5 |
| Completeness | 5 | 2 | 5 |
| Faithfulness | 5 | 3 | 5 |
| Retrieval Prec | 0.80 | 0.75 | 0.57 |
| Retrieval Recall | 1.00 | 0.75 | 1.00 |
| Branching Success | 1 | 0 | 1 |
| Grounded Hop Coverage | 1 | 0.333 | 1 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 0.333 | 1 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 1 | 3 |
| Matched Tools | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 7 | 10 | 9 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Evidence:
- orders table: ORD-109 — status delivered, total_usd = $9,500 (orders).
- customers table: C001 (Northwind Hospitals) — tier = Enterprise (customers).
- incidents table: INC-9003 for ORD-109 — category = pick_pack_error on a delivered order (incidents).
- support_policies.md: "pick_pack_e...
- **LangGraph**: I can’t determine the customer-facing compensation from the data available — there’s no compensation policy or recorded credit/compensation entry in the database tables I can access.

What I can confirm from the records:
- Order: ORD-109 — total $9,500, delivered from WH-ATL on 2026-02-07.
- Custome...
- **smolagents**: Recommendation (grounded in DB + policy):

- Offer: a $760.00 goodwill credit to the customer (account credit or refund as appropriate).
  - Rationale: Incident INC-9003 for ORD-109 is categorized as pick_pack_error (resolved). Policy (support_policies.md) prescribes a goodwill credit for delivered ...

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 9.49 | 6.77 | 101.19 |
| Tokens | 2,472 | 2,161 | 23,801 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 4 | 4 |
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
| Tool Calls Reported | 3 | 3 | 3 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: According to the oncall table, the Commercial team’s on-call engineers are:
- Primary: Omar Santos
- Secondary: Lina Hoffmann
- **LangGraph**: Primary on-call engineer for the Commercial team: Omar Santos.
Secondary on-call engineer: Lina Hoffmann.
- **smolagents**: The current on-call engineer for the Commercial team (primary) is Omar Santos. The secondary engineer is Lina Hoffmann. (Source: oncall table query.)

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 40.74 | 55.84 | 455.46 |
| Tokens | 16,055 | 14,964 | 141,011 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.83 | 1.00 | 0.83 |
| Retrieval Recall | 0.83 | 0.83 | 0.83 |
| Branching Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.333 | 0.333 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 0.667 | 0.667 |
| Is Branching | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 2 | 2 |
| Matched Tools | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 9 | 10 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Recommendation: Keep the issue with Account Support (do not wake the Sev1 commander).

Evidence:
- Support case: CASE-779 for ORD-109 is open, priority = "medium", customer_waiting_hours = 10, last_update_hours = 2 (opened_at 2026-02-08T12:40:00Z). (support_cases)
- Customer: Northwind Hospitals is ...
- **LangGraph**: Recommendation: Keep it with account support (do not wake the Sev1 commander now).

Evidence:
- support_cases: CASE-779 (ORD-109) — priority = medium, status = open, customer_waiting_hours = 10, last_update_hours = 2.  
- incidents: INC-9003 for ORD-109 — severity = P2 and resolved_at = 2026-02-08T1...
- **smolagents**: Recommendation: Wake the Sev1 commander now.

Why (grounded evidence)
- Policy: escalation_matrix.md states "Wake Sev1 commander only when at least one condition is true: 1. Active unresolved P1 incident. 2. Cascading failures across multiple customers. 3. Explicit compliance/legal trigger." support...
