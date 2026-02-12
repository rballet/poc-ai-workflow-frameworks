# Framework Comparison Report

Generated: 2026-02-12 00:00 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: baseline
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 37.46 | 33.24 | 10.82 |
| Total Tokens | 64,387 | 60,300 | 27,012 |
| Est. Cost (USD) | $0.0563 | $0.0553 | $0.0189 |
| Avg Correctness (1-5) | 2.7 | 2.5 | 1.5 |
| Avg Completeness (1-5) | 2.7 | 2.4 | 1.4 |
| Avg Faithfulness (1-5) | 4.8 | 4.6 | 1.7 |
| Avg Retrieval Precision | 0.52 | 0.72 | 0.60 |
| Avg Retrieval Recall | 0.60 | 0.58 | 0.38 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Capability | 68.0 | 63.3 | 30.7 |
| Efficiency | 0.0 | 3.2 | 33.3 |
| Developer Experience | N/A | N/A | N/A |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency p50 (s) | 33.02 | 27.85 | 7.92 |
| Latency p95 (s) | 72.97 | 66.69 | 24.96 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Actual Agents Avg | 1.500 | 1.600 | 1.100 |
| Agent Coverage Avg | 0.750 | 0.767 | 0.633 |
| Coordination Avg Agent Coverage | 0.643 | 0.667 | 0.476 |
| Coordination Avg Grounded Hop Coverage | 0.262 | 0.224 | 0 |
| Coordination Avg Hop Coverage | 0.598 | 0.602 | 0.048 |
| Coordination Avg Tool Coverage | 0.643 | 0.667 | 0.476 |
| Coordination Points Avg | 2.200 | 2.200 | 2.200 |
| Coordination Questions | 7 | 7 | 7 |
| Coordination Success Avg | 0.100 | 0.200 | 0 |
| Coordination Success Rate | 0.143 | 0.286 | 0 |
| Easy Avg Hop Coverage | 0.667 | 0.667 | 0.333 |
| Easy Questions | 3 | 3 | 3 |
| Grounded Hop Coverage Avg | 0.383 | 0.357 | 0.100 |
| Has Tool Trace Avg | 1 | 1 | 1 |
| Hop Coverage Avg | 0.618 | 0.622 | 0.133 |
| Is Coordination Avg | 0.700 | 0.700 | 0.700 |
| Is Easy Avg | 0.300 | 0.300 | 0.300 |
| Matched Hops Avg | 1.800 | 1.800 | 0.200 |
| Matched Tools Avg | 1.400 | 1.500 | 1.100 |
| Required Agents Avg | 2.100 | 2.100 | 2.100 |
| Required Hops Avg | 2.800 | 2.800 | 2.800 |
| Required Tools Count Avg | 2.100 | 2.100 | 2.100 |
| Tool Calls Reported Avg | 2.800 | 2.800 | 1.100 |
| Tool Coverage Avg | 0.750 | 0.767 | 0.633 |
| Tool Trace Rate | 1 | 1 | 1 |

## Per-Question Results

### q1: What services run on the prod-us-east-1 cluster and what are their tiers?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 16.37 | 15.54 | 6.60 |
| Tokens | 6,202 | 6,366 | 2,436 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Actual Agents | 1 | 1 | 1 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0 | 0 | 0 |
| Is Coordination | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 0 | 0 | 0 |
| Matched Tools | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: I confirmed the cluster exists but hit the tool-call limit before I could list its services.

What I was able to verify
- Cluster name prod-us-east-1 exists with cluster_id = CL-001 (queried clusters).
- The services table contains a tier column (I inspected the schema with PRAGMA to confirm the col...
- **LangGraph**: Summary
- I found the cluster prod-us-east-1 in our inventory:
  - cluster_id: CL-001
  - name: prod-us-east-1
  - region: us-east-1
  - environment: production

What I could not complete
- I was not able to retrieve the list of services and their tiers because the tool-call budget was reached befor...
- **smolagents**: Calling tool to inspect clusters table schema to build the correct query.

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 31.77 | 23.54 | 5.95 |
| Tokens | 7,455 | 4,857 | 2,390 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Actual Agents | 2 | 2 | 1 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 |
| Is Coordination | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — there is 1 open critical vulnerability. It is overdue.

Evidence (from vulnerability_scans):
- scan_id: SCAN-201
- service_id: SVC-004
- scanned_at: 2026-02-08T06:00:00Z
- severity: critical
- cve_id: CVE-2025-31337
- description: Remote code execution in container base image
- s...
- **LangGraph**: Yes — there is one open critical vulnerability.

Details
- scan_id: SCAN-201
- severity / status: critical / open
- cve: CVE-2025-31337
- description: Remote code execution in container base image
- service: order-service (service_id SVC-004), team_owner: Commerce, tier: critical
- scanned_at: 2026-...
- **smolagents**: Calling tool to fetch open critical vulnerabilities now.

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 13.87 | 19.31 | 10.03 |
| Tokens | 2,165 | 2,678 | 2,803 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Actual Agents | 1 | 1 | 1 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 |
| Is Coordination | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 |
| Matched Tools | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 |
| Tool Calls Reported | 1 | 1 | 1 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer — escalate a Sev2 to Sev1 if ANY of the following are true:

- Cascading impact detected: the affected service has downstream dependents that are also degraded or failing.  
- Investigating > 60 minutes with no identification: the incident remains in "investigating" status for more than...
- **LangGraph**: Short answer — from the incident response runbook, a Sev2 MUST be promoted to Sev1 if ANY of the following are true:

1. Cascading impact detected — the affected service has downstream dependents that are also degraded.
2. The incident remains in "investigating" status for more than 60 minutes witho...
- **smolagents**: Per the incident response runbook, a Sev2 MUST be promoted to Sev1 if ANY of the following escalation triggers are met:

- Cascading impact detected — the affected service has downstream dependents that are also degraded.  
- Investigation has been in "investigating" status > 60 minutes without iden...

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 42.17 | 29.18 | 10.48 |
| Tokens | 6,119 | 6,665 | 2,384 |
| Correctness | 3 | 1 | 1 |
| Completeness | 3 | 1 | 1 |
| Faithfulness | 4 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 |
| Retrieval Recall | 1.00 | 0.50 | 0.00 |
| Actual Agents | 2 | 1 | 1 |
| Agent Coverage | 1 | 0.500 | 0.500 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0.333 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 0.333 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 1 | 0 |
| Matched Tools | 2 | 1 | 1 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 0.500 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: No — the most recent deploy of auth-service was not compliant with the change management policy.

What I checked (evidence)
- recent_deploys / services record for auth-service (most recent deploy):
  - service_id: SVC-002, tier: critical
  - deploy_id: DEP-102
  - deployed_at: 2026-02-...
- **LangGraph**: Short answer: I cannot determine compliance from the systems I can query — the recent_deploys table contains no record for "auth-service" so there is no deployment metadata I can check against the change-management requirements.

What I checked
- I inspected the recent_deploys schema and then querie...
- **smolagents**: Tool call 1/2: query_infrastructure
</commentary>

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 24.35 | 25.38 | 9.25 |
| Tokens | 5,246 | 5,073 | 2,581 |
| Correctness | 1 | 3 | 1 |
| Completeness | 1 | 3 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 1.00 | 1.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.50 |
| Actual Agents | 1 | 1 | 1 |
| Agent Coverage | 0.500 | 0.500 | 0.500 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0.500 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 0 | 1 | 0 |
| Matched Tools | 1 | 1 | 1 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 2 | 2 | 2 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.500 | 0.500 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: I cannot confirm that FW-404 on prod-eu-west-1 was properly authorized.

What I checked
- I looked for a firewall_rules row for rule_id = 'FW-404' on cluster_id = 'prod-eu-west-1' and there is no matching record in the firewall_rules table.
- The firewall_rules table schema does includ...
- **LangGraph**: Short answer: No evidence that FW-404 was changed on prod-eu-west-1. The only record for FW-404 is for cluster_id CL-002 and it was modified by an automation account — we cannot conclusively say it was “properly authorized” for prod-eu-west-1 without additional audit/change-ticket evidence.

What I ...
- **smolagents**: Calling query_security to find the FW-404 row (one call).

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 34.28 | 26.52 | 31.43 |
| Tokens | 6,506 | 4,198 | 4,258 |
| Correctness | 2 | 1 | 1 |
| Completeness | 2 | 1 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.67 | 0.67 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Actual Agents | 2 | 2 | 2 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.333 | 0.333 | 0.333 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 1 | 1 | 1 |
| Matched Tools | 2 | 2 | 2 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 2 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: I can do that, but I can’t finish the query right now because I’ve already used the allowed tool calls for this session (I ran schema PRAGMAs). To produce a grounded list I need one query against the vulnerability_scans + recent_deploys (and services) tables. Below I show:

- what I would look for (...
- **LangGraph**: I don’t yet have the data needed to produce a grounded list — the schema for the relevant tables is available, but I haven’t queried the vulnerability or recent-deploy rows themselves. To answer precisely I need to run two queries (one against the security scans, one against recent_deploys) and inte...
- **smolagents**: I don’t yet have the query results because the previous attempt used the wrong column name. To get a grounded answer I need to run one SQL query that joins services, vulnerability_scans and recent_deploys. Here’s the correct query (it uses the actual column names shown in the schema):

SQL to run:
S...

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 52.04 | 31.99 | 6.48 |
| Tokens | 7,687 | 7,463 | 2,492 |
| Correctness | 5 | 3 | 1 |
| Completeness | 4 | 2 | 1 |
| Faithfulness | 5 | 3 | 1 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.33 | 0.33 | 0.17 |
| Actual Agents | 2 | 1 | 1 |
| Agent Coverage | 0.667 | 0.333 | 0.333 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.250 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.750 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 2 | 0 |
| Matched Tools | 2 | 1 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.667 | 0.333 | 0.333 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: a latency/regression introduced by the auth-service deployment (v2.4.1-rc3 at 16:30) that caused upstream auth calls to hit p99 latencies ~8200ms, making payment-service requests fail with 503s.
- Was incident response proper? Partially — initial detection and comma...
- **LangGraph**: Short answer
- Most likely root cause: the auth-service deploy introduced a breaking change or outage that caused payment-service’s upstream auth calls to fail, producing 503s (temporal correlation in the incident title strongly suggests the new auth build caused payment-service to get upstream 503 ...
- **smolagents**: Calling tools:
[{'id': 'call_qjhF17uwbYSxob9sbsyt3WhN', 'type': 'function', 'function': {'name': 'query_infrastructure', 'arguments': {'query': "SELECT * FROM incidents WHERE incident_id = 'INC-4001';"}}}]

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 90.10 | 75.04 | 17.05 |
| Tokens | 9,420 | 9,406 | 3,086 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 2 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.00 | 0.50 | 0.00 |
| Retrieval Recall | 0.00 | 0.14 | 0.00 |
| Actual Agents | 2 | 3 | 1 |
| Agent Coverage | 0.667 | 1 | 0.333 |
| Coordination Points | 5 | 5 | 5 |
| Coordination Success | 0 | 1 | 0 |
| Grounded Hop Coverage | 0 | 0.400 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.600 | 0.800 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 4 | 0 |
| Matched Tools | 2 | 3 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 5 | 5 | 5 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.667 | 1 | 0.333 |

**Answers:**

- **Pydantic AI**: Short version / status
- I could not retrieve INC-4002 records — the tooling hit the 3-call budget before we returned incident data. I therefore cannot state a definitive, evidence-backed root cause or exact compliance violations for INC-4002.
- Below I give: (A) the minimum queries / checks to run ...
- **LangGraph**: Short version / bottom line
- I could not retrieve incident-specific records for INC-4002 because the read-only queries were not executed (tool budget exhausted). I therefore can’t state a confirmed root cause or list actual security/compliance findings — only a prioritized, evidence-driven analysis...
- **smolagents**: Calling tool to fetch incident, timeline, service, deploy and cluster details for INC-4002 (1/3)...

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 39.27 | 29.45 | 5.03 |
| Tokens | 5,693 | 5,374 | 2,095 |
| Correctness | 3 | 3 | 2 |
| Completeness | 3 | 2 | 1 |
| Faithfulness | 4 | 3 | 4 |
| Retrieval Prec | 0.00 | 0.50 | 0.00 |
| Retrieval Recall | 0.00 | 0.14 | 0.00 |
| Actual Agents | 1 | 1 | 1 |
| Agent Coverage | 0.333 | 0.333 | 0.333 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.750 | 0.750 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 |
| Matched Tools | 1 | 1 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.333 | 0.333 | 0.333 |

**Answers:**

- **Pydantic AI**: Short answer (summary)
- Immediate containment: block/restrict 198.51.100.0/24 and/or remove FW-404 — approval: incident commander (dave@nimbusops.io) or on-call network engineer with explicit emergency change authorization from the incident commander/security lead.
- Investigation & evidence collec...
- **LangGraph**: Short answer
- High-level sequence: 1) Confirm & contain → 2) Mitigate (quick fix) → 3) Identify root cause → 4) Remediate (rollback/patch/scale/config change) → 5) Validate & monitor → 6) Close & follow-up (postmortem).
- Who must approve: immediate mitigations can be authorized by the Incident Com...
- **smolagents**: I looked up INC-4002 (order-service degraded performance in eu-west-1; sev2; investigating; commander dave@nimbusops.io). To recommend a grounded remediation sequence and who must approve, I need two pieces of info: the service runbook/playbook for SVC-004 (order-service) and the approval policy for...

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 30.40 | 56.49 | 5.88 |
| Tokens | 7,894 | 8,220 | 2,487 |
| Correctness | 1 | 2 | 1 |
| Completeness | 2 | 2 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 1.00 | 1.00 |
| Retrieval Recall | 0.17 | 0.17 | 0.17 |
| Actual Agents | 1 | 3 | 1 |
| Agent Coverage | 0.333 | 1 | 0.333 |
| Coordination Points | 3 | 3 | 3 |
| Coordination Success | 0 | 1 | 0 |
| Grounded Hop Coverage | 0.250 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.750 | 1 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 4 | 0 |
| Matched Tools | 1 | 3 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.333 | 1 | 0.333 |

**Answers:**

- **Pydantic AI**: Short answer
- Not yet — there isn’t enough evidence in the data we currently have to justify escalating INC-4002 from sev2 → sev1. The incident metadata shows a sev2 investigating ticket opened ~24 hours ago, but we’re missing the operational and policy evidence required to justify an escalation.

...
- **LangGraph**: Short answer: I cannot confidently recommend escalating INC-4002 from sev2 → sev1 with the current evidence available. The incident runbook defines clear, objective escalation triggers (see below), but I don’t have the incident’s details (status, timestamps, timeline entries, access-log anomaly scor...
- **smolagents**: I will check the incident record and the escalation policy to decide. I'll need to look up INC-4002 and the severity/escalation policy. May I query the incidents database and the policy table?
