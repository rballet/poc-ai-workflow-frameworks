# Framework Comparison Report

Generated: 2026-02-11 01:10 UTC
Scenario: agentic_sql_qa
Scenario Type: agentic_tool_qa
Mode: baseline
Profile: tool_branching_qa
Questions: 8

## Summary

| Metric | LangGraph |
| --- | --- |
| Avg Latency (s) | 3.70 |
| Total Tokens | 5,383 |
| Est. Cost (USD) | $0.0013 |
| Avg Correctness (1-5) | 1.5 |
| Avg Completeness (1-5) | 1.5 |
| Avg Faithfulness (1-5) | 2.5 |
| Avg Retrieval Precision | 0.50 |
| Avg Retrieval Recall | 0.28 |

## Scenario-Specific Metrics

| Metric | LangGraph |
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
| Has Tool Trace Avg | 1 |
| Hop Coverage Avg | 0.458 |
| Is Branching Avg | 0.500 |
| Is Easy Avg | 0.500 |
| Matched Hops Avg | 0.625 |
| Matched Tools Avg | 1 |
| Required Hops Avg | 2 |
| Required Tools Avg | 1.500 |
| Tool Calls Reported Avg | 1 |
| Tool Coverage Avg | 0.750 |
| Tool Trace Rate | 1 |

## Per-Question Results

### q1: What account tier and operating region does Acme Health belong to?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 3.78 |
| Tokens | 487 |
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

- **LangGraph**: The evidence is insufficient to determine the account tier and operating region for Acme Health because the relevant table "accounts" does not exist in the provided schema. The available tables do not contain the necessary information about Acme Health.

### q2: Are weather-related shipment delays eligible for shipping credits?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 3.16 |
| Tokens | 761 |
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

- **LangGraph**: No, weather-related shipment delays are not eligible for shipping credits. According to the Shipping Credit Policy, a delivery delay must be **not** due to weather, customs hold, or force majeure to qualify for a shipping credit.

### q3: How many unresolved P1 incidents are currently open?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 3.41 |
| Tokens | 522 |
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

- **LangGraph**: The evidence is missing the necessary information to determine the number of unresolved P1 incidents because the column "priority" does not exist in the "incidents" table. Instead, the "priority" column is found in the "support_cases" table. To answer the question, a query should be run on the "supp...

### q4: Can order ORD-104 receive a shipping credit, and what is the maximum amount?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 2.43 |
| Tokens | 448 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 3 |
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

- **LangGraph**: The evidence does not provide information regarding whether order ORD-104 can receive a shipping credit or the maximum amount of such a credit. Specifically, details about shipping credit eligibility and limits are missing.

### q5: Should CASE-778 be auto-escalated, and which team should own it?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 5.59 |
| Tokens | 868 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 3 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.40 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.333 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **LangGraph**: To determine if CASE-778 should be auto-escalated and which team should own it, we need specific details about the case, such as its priority level (P1 or otherwise), the type of incident it pertains to (e.g., payment_gateway, fraud_review), and whether it involves an enterprise customer.

Currently...

### q6: For order ORD-109, what customer-facing compensation should be offered?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 3.81 |
| Tokens | 835 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 3 |
| Retrieval Prec | 0.50 |
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

- **LangGraph**: To determine the customer-facing compensation for order ORD-109, we need to know the following:

1. The status of the order (it must be `delivered`).
2. The duration of any delivery delay (it must be **24 hours or more**).
3. The reason for the delay (it must be **not** due to weather, customs hold,...

### q7: Who is the current on-call engineer for the Commercial team?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 3.29 |
| Tokens | 515 |
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

- **LangGraph**: The evidence is missing the current on-call engineer for the Commercial team because the query attempted to access a non-existent table called "on_call_schedule." Instead, the relevant table is "oncall," which contains the information about the on-call engineers. Please provide the correct query to ...

### q8: Northwind Hospitals has an open issue on ORD-109. Should we wake the Sev1 commander now, or keep it with account support?

| Metric | LangGraph |
| --- | --- |
| Latency (s) | 4.10 |
| Tokens | 947 |
| Correctness | 1 |
| Completeness | 1 |
| Faithfulness | 3 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.33 |
| Branching Success | 0 |
| Grounded Hop Coverage | 0 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.333 |
| Is Branching | 1 |
| Is Easy | 0 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Hops | 3 |
| Required Tools | 2 |
| Tool Calls Reported | 1 |
| Tool Coverage | 0.500 |

**Answers:**

- **LangGraph**: To determine whether to wake the Sev1 commander for ORD-109, we need to check if there is an active unresolved P1 incident or if there are cascading failures across multiple customers. 

The evidence does not specify whether ORD-109 is classified as a P1 incident or if there are any cascading failur...
