# Framework Comparison Report

Generated: 2026-02-12 22:55 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: capability
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Latency (s) | 14.55 | 12.45 | 95.62 | 27.87 |
| Total Tokens | 83,930 | 68,735 | 121,188 | 82,740 |
| Est. Cost (USD) | $0.0336 | $0.0272 | $0.0762 | $0.0578 |
| Avg Correctness (1-5) | 4.8 | 5.0 | 2.5 | 5.0 |
| Avg Completeness (1-5) | 4.6 | 5.0 | 2.5 | 4.6 |
| Avg Faithfulness (1-5) | 5.0 | 5.0 | 2.5 | 4.8 |
| Avg Retrieval Precision | 0.85 | 0.85 | 0.33 | 0.86 |
| Avg Retrieval Recall | 0.93 | 0.98 | 0.50 | 0.96 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Capability | 67.7 | 77.1 | 12.5 | 59.4 |
| Efficiency | 29.3 | 33.3 | 0.0 | 20.8 |
| Developer Experience | 85.8 | 30.7 | 80.4 | 94.4 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency p50 (s) | 13.12 | 8.97 | 106.53 | 23.46 |
| Latency p95 (s) | 26.31 | 24.90 | 120.00 | 49.67 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Branching Avg Grounded Hop Coverage | 0.750 | 0.750 | 0 | 0.500 |
| Branching Avg Hop Coverage | 0.750 | 0.833 | 0 | 0.667 |
| Branching Avg Tool Coverage | 0.875 | 1 | 0 | 1 |
| Branching Questions | 4 | 4 | 4 | 4 |
| Branching Success Avg | 0.125 | 0.250 | 0 | 0.125 |
| Branching Success Rate | 0.250 | 0.500 | 0 | 0.250 |
| Easy Avg Hop Coverage | 1 | 1 | 1 | 1 |
| Easy Questions | 4 | 4 | 4 | 4 |
| Grounded Hop Coverage Avg | 0.875 | 0.875 | 0.500 | 0.750 |
| Has Tool Trace Avg | 1 | 1 | 0.500 | 1 |
| Hop Coverage Avg | 0.875 | 0.917 | 0.500 | 0.833 |
| Is Branching Avg | 0.500 | 0.500 | 0.500 | 0.500 |
| Is Easy Avg | 0.500 | 0.500 | 0.500 | 0.500 |
| Matched Hops Avg | 1.625 | 1.750 | 0.500 | 1.500 |
| Matched Tools Avg | 1.375 | 1.500 | 0.500 | 1.500 |
| Required Hops Avg | 2 | 2 | 2 | 2 |
| Required Tools Avg | 1.500 | 1.500 | 1.500 | 1.500 |
| Tool Calls Reported Avg | 6.125 | 5.500 | 2.125 | 4.625 |
| Tool Coverage Avg | 0.938 | 1 | 0.500 | 1 |
| Tool Trace Rate | 1 | 1 | 0.500 | 1 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Source Lines (SLOC) | 134 | 183 | 203 | 156 |
| Comment Ratio | 0% | 0% | 1% | 0% |
| Avg Cyclomatic Complexity | 2.2 | 3.2 | 2.5 | 2.4 |
| Max Cyclomatic Complexity | 6 | 10 | 10 | 7 |
| Complexity Grade | A | A | A | A |
| Maintainability Index | 40.0 | 32.2 | 42.3 | 45.8 |
| Maintainability Grade | A | A | A | A |
| Halstead Volume | 175 | 247 | 221 | 204 |
| Halstead Difficulty | 3.8 | 5.5 | 5.5 | 4.5 |
| Halstead Bugs (est.) | 0.06 | 0.08 | 0.07 | 0.07 |
| Total Imports | 8 | 13 | 10 | 9 |
| Framework Imports | 1 | 6 | 1 | 0 |
| Classes | 2 | 1 | 3 | 5 |
| Functions | 9 | 13 | 10 | 8 |
| Type Annotation Coverage | 100% | 92% | 100% | 100% |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 5.47 | 4.42 | 58.21 | 13.52 |
| Tokens | 3,124 | 2,489 | 22,573 | 4,703 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 4 | 3 | 3 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Acme Health is an Enterprise-tier account operating in the us-west region. Evidence: customers table row for "Acme Health" (tier = "Enterprise", region = "us-west").
- **LangGraph**: Acme Health is in the Enterprise tier and operates in the us-west region.
- **smolagents**: Acme Health belongs to the Enterprise account tier and operates in the us-west region. (Source: customers table — customer_id C003, row: name='Acme Health', tier='Enterprise', region='us-west', owner_team='Strategic Accounts'.)
- **CrewAI**: From the customers table:
- customer_id: C003
- name: Acme Health
- tier: Enterprise
- region: us-west

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 6.11 | 5.06 | 54.95 | 21.98 |
| Tokens | 1,370 | 1,432 | 18,573 | 3,698 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 4 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 1 | 1 | 2 | 1 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: No. Per the Shipping Credit Policy, weather-related delays are excluded.

Evidence (Support Policies — Shipping Credit Policy):
- Eligibility requires: status = delivered; delivery delay ≥ 24 hours; and delay reason is NOT weather, customs hold, or force majeure.
- (The policy also lists credit caps...
- **LangGraph**: No. According to the Shipping Credit Policy (support_policies.md), weather-related delays are excluded. The policy states credits apply only when:
- Status is delivered,
- Delivery delay is 24 hours or more, and
- Delay reason is not weather, customs hold, or force majeure.

Credit caps by account t...
- **smolagents**: Short answer: No — weather-related shipment delays are not eligible for shipping credits.

Grounding and details (policy citations):
- Support Policies — Shipping Credit Policy: “An order is eligible for a shipping credit when all of the following are true: 1. Status is `delivered`. 2. Delivery dela...
- **CrewAI**: No — weather-related shipment delays are not eligible for shipping credits.

Full policy excerpt (source: Support Policies — Shipping Credit Policy):

## Shipping Credit Policy

An order is eligible for a shipping credit when all of the following are true:

1. Status is `delivered`.
2. Delivery dela...

### q3: How many unresolved P1 incidents are currently open?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 6.40 | 3.94 | 93.06 | 10.63 |
| Tokens | 2,805 | 2,412 | 42,026 | 4,437 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 5 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: There are 2 unresolved P1 incidents currently open.

Query used:
SELECT COUNT(*) AS unresolved_p1 FROM incidents WHERE severity = 'P1' AND resolved_at IS NULL;
- **LangGraph**: There are 2 unresolved P1 incidents currently open.
- **smolagents**: There are 2 unresolved P1 incidents currently open.

Evidence (from database queries):
- Count query: SELECT COUNT(*) AS count FROM incidents WHERE severity = 'P1' AND (resolved_at IS NULL OR resolved_at = '');  Result: 2
- Rows (SELECT incident_id, opened_at, resolved_at FROM incidents WHERE severi...
- **CrewAI**: There are 2 unresolved P1 incidents currently open.

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 17.68 | 12.88 | 120.00 | 35.94 |
| Tokens | 12,947 | 9,907 | 0 | 10,373 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 5 | 0 | 5 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 0.80 | 0.80 | 0.00 | 0.80 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.667 | 0 | 0.667 |
| Has Tool Trace | 1 | 1 | 0 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0 | 0.667 |
| Is Branching | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 0 | 2 |
| Matched Tools | 2 | 2 | 0 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 8 | 7 | 0 | 5 |
| Tool Coverage | 1 | 1 | 0 | 1 |

**Answers:**

- **Pydantic AI**: Yes — ORD-104 is eligible for a shipping credit.

Evidence:
- orders row: status = "delivered", total_usd = 7000.00 (orders table).
- shipments row: delay_hours = 30, delay_reason = "carrier_misroute" (shipments table).
- customer row: tier = "Enterprise" (customers table).
- Shipping Credit Policy:...
- **LangGraph**: Yes. Evidence and calculation:

- Order ORD-104: status = delivered; total = $7,000. (orders table)
- Shipment: delay = 30 hours; delay_reason = carrier_misroute. (shipments table)
- Customer C003 tier = Enterprise. (customers table)
- Shipping Credit Policy: eligible if delivered, delay ≥ 24 hours,...
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: Evidence from the database and policy:

- orders row (run_sql):
  - order_id: ORD-104
  - customer_id: C003
  - status: delivered
  - total_usd: 7000.0

- shipments row (run_sql):
  - order_id: ORD-104
  - delay_hours: 30
  - delay_reason: carrier_misroute

- customers row (run_sql):
  - customer_id...

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 28.23 | 19.17 | 120.00 | 44.97 |
| Tokens | 21,598 | 13,461 | 0 | 21,529 |
| Correctness | 3 | 5 | 0 | 5 |
| Completeness | 3 | 5 | 0 | 3 |
| Faithfulness | 5 | 5 | 0 | 4 |
| Retrieval Prec | 0.80 | 1.00 | 0.00 | 1.00 |
| Retrieval Recall | 0.80 | 1.00 | 0.00 | 1.00 |
| Branching Success | 0 | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 1 | 0 | 0.333 |
| Has Tool Trace | 1 | 1 | 0 | 1 |
| Hop Coverage | 0.667 | 1 | 0 | 0.333 |
| Is Branching | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 3 | 0 | 1 |
| Matched Tools | 2 | 2 | 0 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 8 | 0 | 8 |
| Tool Coverage | 1 | 1 | 0 | 1 |

**Answers:**

- **Pydantic AI**: Yes — CASE-778 should be auto‑escalated.

Grounding/evidence
- support_cases: CASE-778 is high priority, open, customer_waiting_hours = 26 (hours) and last_update_hours = 7. (support_cases row)
- customers: customer C003 (Acme Health) is tier = Enterprise and owner_team = Strategic Accounts. (custom...
- **LangGraph**: Yes — CASE-778 should be auto‑escalated immediately.

Evidence (from the database)
- support_cases: CASE-778 is high priority, customer_waiting_hours = 26, last_update_hours = 7.  
- customers: C003 (Acme Health) is Enterprise and owner_team = "Strategic Accounts".  
- incidents: ORD-102 has an acti...
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: CASE-778 should be auto-escalated. Primary ownership: Platform Reliability (eng_oncall_1, eng1@company.com). Notify/keep Strategic Accounts (acct_oncall_2, acct2@company.com) in the loop because this is an enterprise customer (Acme Corp) with order value $15,200 (> $10,000). Evidence: include releva...

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 21.23 | 24.04 | 120.00 | 24.95 |
| Tokens | 21,526 | 21,071 | 0 | 16,141 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 5 | 0 | 5 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 0.67 | 0.67 | 0.00 | 0.80 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Branching Success | 1 | 1 | 0 | 1 |
| Grounded Hop Coverage | 1 | 1 | 0 | 1 |
| Has Tool Trace | 1 | 1 | 0 | 1 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Branching | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 | 3 |
| Matched Tools | 2 | 2 | 0 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 10 | 0 | 7 |
| Tool Coverage | 1 | 1 | 0 | 1 |

**Answers:**

- **Pydantic AI**: Offer a goodwill credit of 8% of the order total = 0.08 * $9,500 = $760.

Why:
- Order ORD-109 is delivered and has an incident with category = pick_pack_error (INC-9003).
- Support policy: pick_pack_error on delivered orders → goodwill credit: Enterprise = 8% of order total.
- Customer Northwind Ho...
- **LangGraph**: From the records and policy:

- Order ORD-109: total_usd = $9,500 (orders table).
- Customer C001 (Northwind Hospitals) is Enterprise (customers table).
- Incident on ORD-109 is category = pick_pack_error and order is delivered (incidents table).
- Policy: "pick_pack_error on delivered orders: goodw...
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: Offer a goodwill credit of $760.00 to the customer.

Evidence from tools:
- Order ORD-109: total_usd = 9500.0, status = delivered (orders table).
- Customer C001 (Northwind Hospitals): tier = Enterprise (customers table).
- Incident INC-9003 on ORD-109: category = pick_pack_error (incidents table).
...

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 8.57 | 4.76 | 78.72 | 18.76 |
| Tokens | 2,648 | 2,164 | 38,016 | 4,974 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 4 |
| Retrieval Prec | 1.00 | 1.00 | 0.17 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 1 |
| Is Branching | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 7 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: The on-call primary for the Commercial team is Omar Santos. (Backup/secondary is Lina Hoffmann — source: oncall table.)
- **LangGraph**: The current primary on-call engineer for the Commercial team is Omar Santos (secondary: Lina Hoffmann).
- **smolagents**: Current on-call engineer for the Commercial team: Omar Santos (primary on-call). Backup/secondary: Lina Hoffmann.

Evidence:
- oncall table row for team = 'Commercial' returned primary_engineer = "Omar Santos" and secondary_engineer = "Lina Hoffmann".
- escalation_matrix.md states: "The `oncall` tab...
- **CrewAI**: The Commercial team on-call engineers are:
- Primary engineer: Omar Santos
- Secondary engineer: Lina Hoffmann

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 22.75 | 25.36 | 120.00 | 52.19 |
| Tokens | 17,912 | 15,799 | 0 | 16,885 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 5 | 0 | 4 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 1.00 | 0.83 | 0.00 | 0.80 |
| Retrieval Recall | 0.67 | 0.83 | 0.00 | 0.67 |
| Branching Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.333 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 0 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0 | 0.667 |
| Is Branching | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 0 | 2 |
| Matched Tools | 1 | 2 | 0 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 10 | 9 | 0 | 7 |
| Tool Coverage | 0.500 | 1 | 0 | 1 |

**Answers:**

- **Pydantic AI**: Recommendation: keep it with account support for now — do not wake the Sev1 commander.

Evidence:
- Incident for ORD-109: INC-9003, severity = P2, category = pick_pack_error, opened 2026-02-08T11:00:00Z, resolved_at = 2026-02-08T12:30:00Z.
- Support case for ORD-109: CASE-779, priority = medium, sta...
- **LangGraph**: Summary of evidence
- incidents table: ORD-109 → incident INC-9003, severity = P2, category = pick_pack_error, opened 2026-02-08T11:00Z, resolved_at = 2026-02-08T12:30:00Z (so the incident record is resolved).  
- orders table: ORD-109 total_usd = 9500.0, status = delivered.  
- customers table: C00...
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: Keep the case with account support — do NOT wake the Sev1 commander now.

Evidence from the database:
- support_cases for ORD-109:
  {
    "case_id": "CASE-779",
    "customer_id": "C001",
    "order_id": "ORD-109",
    "priority": "medium",
    "status": "open",
    "opened_at": "2026-02-08T12:40:0...
