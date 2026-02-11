# Framework Comparison Report

Generated: 2026-02-11 21:06 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: baseline
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | Pydantic AI |
| --- | --- |
| Avg Latency (s) | 32.52 |
| Total Tokens | 24,233 |
| Est. Cost (USD) | $0.0309 |
| Avg Correctness (1-5) | 1.6 |
| Avg Completeness (1-5) | 1.5 |
| Avg Faithfulness (1-5) | 4.1 |
| Avg Retrieval Precision | 0.12 |
| Avg Retrieval Recall | 0.16 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI |
| --- | --- |
| Capability | 18.3 |
| Efficiency | 33.3 |
| Developer Experience | 95.0 |

## Runtime Distribution

| Metric | Pydantic AI |
| --- | --- |
| Latency p50 (s) | 30.30 |
| Latency p95 (s) | 54.19 |

## Scenario-Specific Metrics

| Metric | Pydantic AI |
| --- | --- |
| Branching Avg Grounded Hop Coverage | 0.083 |
| Branching Avg Hop Coverage | 0.167 |
| Branching Avg Tool Coverage | 0.750 |
| Branching Questions | 4 |
| Branching Success Avg | 0 |
| Branching Success Rate | 0 |
| Easy Avg Hop Coverage | 0.750 |
| Easy Questions | 4 |
| Grounded Hop Coverage Avg | 0.167 |
| Has Tool Trace Avg | 1 |
| Hop Coverage Avg | 0.458 |
| Is Branching Avg | 0.500 |
| Is Easy Avg | 0.500 |
| Matched Hops Avg | 0.625 |
| Matched Tools Avg | 1.250 |
| Required Hops Avg | 2 |
| Required Tools Avg | 1.500 |
| Tool Calls Reported Avg | 1 |
| Tool Coverage Avg | 0.875 |
| Tool Trace Rate | 1 |

## Code Quality — Static Metrics

| Metric | Pydantic AI |
| --- | --- |
| Source Lines (SLOC) | 132 |
| Comment Ratio | 0% |
| Avg Cyclomatic Complexity | 2.2 |
| Max Cyclomatic Complexity | 6 |
| Complexity Grade | A |
| Maintainability Index | 40.0 |
| Maintainability Grade | A |
| Halstead Volume | 175 |
| Halstead Difficulty | 3.8 |
| Halstead Bugs (est.) | 0.06 |
| Total Imports | 8 |
| Framework Imports | 1 |
| Classes | 2 |
| Functions | 9 |
| Type Annotation Coverage | 100% |

## Code Quality — LLM Code Review

| Criterion | Pydantic AI |
| --- | --- |
| Readability | 5 |
| Idiomatic Usage | 4 |
| Error Handling | 3 |
| Extensibility | 4 |
| Testability | 4 |
| Documentation | 4 |
| Abstraction | 4 |
| **Average** | 4.0 |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 13.23 |
| Tokens | 1,794 |
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

- **Pydantic AI**: I can't determine Acme Health's account tier or operating region from the evidence available. The only tool result I could retrieve shows the database contains a customers table (plus others), but I did not get any customer rows or the customers table schema.

Evidence collected:
- Tables present: c...

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 19.85 |
| Tokens | 1,351 |
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

- **Pydantic AI**: No. The Shipping Credit Policy explicitly excludes weather as an eligible delay reason.

Evidence from policy:
- Eligibility requires: (1) status = delivered, (2) delivery delay ≥ 24 hours, and (3) delay reason is not weather, customs hold, or force majeure.

### q3: How many unresolved P1 incidents are currently open?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 26.10 |
| Tokens | 2,234 |
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

- **Pydantic AI**: I couldn’t return a count because my first query used a non‑existent column (incidents.priority). The schema shows priority and status live in the support_cases table (support_cases: case_id, customer_id, order_id, priority, status, opened_at, ...).

I can get the number if you want me to run a quer...

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 40.04 |
| Tokens | 3,290 |
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
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **Pydantic AI**: I can’t determine whether ORD-104 can receive a shipping credit or the maximum amount from the evidence available: my only tool call returned the database schema (tables and columns) but did not return any rows for order ORD-104 or any shipping-credit policy data.

What I inspected (from the schema ...

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 45.20 |
| Tokens | 3,449 |
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

- **Pydantic AI**: I can’t tell from available evidence whether CASE-778 should be auto‑escalated because the case row itself was not retrieved. My attempted query targeted a non‑existent table; the database schema shows the correct tables and columns but I don’t have the CASE-778 record.

What I do have (from schema ...

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 59.03 |
| Tokens | 5,409 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 5 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 0.25 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0.333 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.667 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 2 |
| Matched Tools | 2 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: I don’t have the order details for ORD-109 available from the tools called, so I can’t say exactly what to offer. To determine the customer-facing compensation I need these order fields:

- incident_type (e.g., payment_gateway, fraud_review, pick_pack_error, etc.)  
- order status (delivered, failed...

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 22.23 |
| Tokens | 3,150 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 2 |
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

- **Pydantic AI**: I don't have the on-call engineer listed in the evidence I retrieved. From the database schema I can confirm there is an oncall table with columns (team, primary_engineer, secondary_engineer), but I did not fetch the table rows.

If you want me to look up the current Commercial on-call, I need one q...

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 34.51 |
| Tokens | 3,556 |
| Correctness | 2 |
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
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **Pydantic AI**: I can’t determine whether to wake the Sev1 commander from the data I can access right now — my only successful query returned the list of available tables (customers, incidents, oncall, orders, shipments, support_cases) and I do not have any details for ORD-109. I’ve used the one-call budget allowed...
