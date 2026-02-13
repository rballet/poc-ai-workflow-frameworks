# Framework Comparison Report

Generated: 2026-02-12 19:19 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: baseline
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | CrewAI |
| --- | --- |
| Avg Latency (s) | 39.87 |
| Total Tokens | 26,829 |
| Est. Cost (USD) | $0.0379 |
| Avg Correctness (1-5) | 1.5 |
| Avg Completeness (1-5) | 1.5 |
| Avg Faithfulness (1-5) | 3.4 |
| Avg Retrieval Precision | 0.31 |
| Avg Retrieval Recall | 0.20 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | CrewAI |
| --- | --- |
| Capability | 14.8 |
| Efficiency | 33.3 |
| Developer Experience | 100.0 |

## Runtime Distribution

| Metric | CrewAI |
| --- | --- |
| Latency p50 (s) | 28.38 |
| Latency p95 (s) | 93.02 |

## Scenario-Specific Metrics

| Metric | CrewAI |
| --- | --- |
| Branching Avg Grounded Hop Coverage | 0 |
| Branching Avg Hop Coverage | 0.167 |
| Branching Avg Tool Coverage | 0.500 |
| Branching Questions | 4 |
| Branching Success Avg | 0 |
| Branching Success Rate | 0 |
| Easy Avg Hop Coverage | 0.750 |
| Easy Questions | 4 |
| Grounded Hop Coverage Avg | 0.125 |
| Has Tool Trace Avg | 0.875 |
| Hop Coverage Avg | 0.458 |
| Is Branching Avg | 0.500 |
| Is Easy Avg | 0.500 |
| Matched Hops Avg | 0.625 |
| Matched Tools Avg | 1 |
| Required Hops Avg | 2 |
| Required Tools Avg | 1.500 |
| Tool Calls Reported Avg | 0.875 |
| Tool Coverage Avg | 0.750 |
| Tool Trace Rate | 0.875 |

## Code Quality — Static Metrics

| Metric | CrewAI |
| --- | --- |
| Source Lines (SLOC) | 156 |
| Comment Ratio | 0% |
| Avg Cyclomatic Complexity | 2.4 |
| Max Cyclomatic Complexity | 7 |
| Complexity Grade | A |
| Maintainability Index | 45.8 |
| Maintainability Grade | A |
| Halstead Volume | 204 |
| Halstead Difficulty | 4.5 |
| Halstead Bugs (est.) | 0.07 |
| Total Imports | 9 |
| Framework Imports | 0 |
| Classes | 5 |
| Functions | 8 |
| Type Annotation Coverage | 100% |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 23.46 |
| Tokens | 3,499 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 5 |
| Retrieval Prec | 0.00 |
| Retrieval Recall | 0.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Branching | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Hops | 1 |
| Required Tools | 1 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **CrewAI**: I could not find Acme Health's account tier and operating region from the available evidence. To obtain them, run this query against the database:

SELECT tier, region FROM customers WHERE name = 'Acme Health';

If the exact name may differ, try:

SELECT tier, region, name FROM customers WHERE name ...

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 14.47 |
| Tokens | 2,518 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 1.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Branching | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Hops | 1 |
| Required Tools | 1 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **CrewAI**: # Support Policies

## Shipping Credit Policy

An order is eligible for a shipping credit when all of the following are true:

1. Status is `delivered`.
2. Delivery delay is **24 hours or more**.
3. Delay reason is **not** weather, customs hold, or force majeure.

Credit caps by account tier:

- Ent...

### q3: How many unresolved P1 incidents are currently open?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 30.96 |
| Tokens | 3,766 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 1 |
| Retrieval Prec | 0.00 |
| Retrieval Recall | 0.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0 |
| Is Branching | 0 |
| Is Easy | 1 |
| Matched Hops | 0 |
| Matched Tools | 1 |
| Required Hops | 1 |
| Required Tools | 1 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **CrewAI**: I cannot determine the number of unresolved P1 incidents because I was unable to run a successful query against the table that contains priority (the earlier query failed: incidents has no priority column). The schema evidence shows the relevant fields exist in support_cases (support_cases: case_id,...

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 120.00 |
| Tokens | 0 |
| Correctness | 0 |
| Completeness | 0 |
| Faithfulness | 0 |
| Retrieval Prec | 0.00 |
| Retrieval Recall | 0.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 0 |
| Hop Coverage | 0 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 0 |
| Matched Tools | 0 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 0 |
| Tool Coverage | 0 |

**Answers:**

- **CrewAI**: Query timed out before producing an answer.

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 42.92 |
| Tokens | 4,903 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 5 |
| Retrieval Prec | 0.00 |
| Retrieval Recall | 0.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 0 |
| Matched Tools | 2 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **CrewAI**: I cannot determine whether CASE-778 should be auto-escalated or which team should own it because I could not retrieve any policy documents or case data — the single allowed tool call (lookup_doc) exhausted the tool-call budget and returned no usable evidence.

What is missing (explicit list of requi...

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 25.80 |
| Tokens | 3,439 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.25 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 0 |
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **CrewAI**: I queried the orders table for ORD-109. The database record I found:

- order_id: ORD-109
- customer_id: C001
- created_at: 2026-02-07T09:00:00Z
- total_usd: 9500.0
- status: delivered
- warehouse: WH-ATL

There is no information in that record about an issue, return, refund, or any compensation alr...

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 25.05 |
| Tokens | 3,673 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 1 |
| Retrieval Prec | 0.00 |
| Retrieval Recall | 0.00 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Branching | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Hops | 1 |
| Required Tools | 1 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **CrewAI**: The database schema includes an oncall table with columns (team, primary_engineer, secondary_engineer), but I did not retrieve its rows — the current on-call engineer for the Commercial team is not available from the evidence gathered. To determine the current on-call engineer, run this query agains...

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 36.29 |
| Tokens | 5,031 |
| Correctness | 2 |
| Completeness | 2 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.33 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.667 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 2 |
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **CrewAI**: I do not have any case-specific evidence (severity, age, whether multiple customers are affected, compliance/legal trigger, or order value/account tier) for ORD-109, so I cannot unambiguously decide to wake the Sev1 commander. Policy guidance from the support docs (verbatim from the policy search re...
