# Framework Comparison Report

Generated: 2026-02-13 00:24 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: capability
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Latency (s) | 77.27 | 125.13 | 156.00 | 284.82 |
| Total Tokens | 322,081 | 942,719 | 0 | 2,516,016 |
| Est. Cost (USD) | $0.2847 | $0.3897 | $0.0000 | $3.0631 |
| Avg Correctness (1-5) | 4.9 | 3.6 | 1.0 | 0.2 |
| Avg Completeness (1-5) | 4.4 | 3.6 | 1.0 | 0.2 |
| Avg Faithfulness (1-5) | 4.9 | 3.9 | 1.0 | 0.2 |
| Avg Retrieval Precision | 0.35 | 0.53 | 0.32 | 0.10 |
| Avg Retrieval Recall | 0.94 | 0.84 | 0.84 | 0.05 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Capability | 94.7 | 74.0 | 20.0 | 4.0 |
| Efficiency | 31.2 | 26.1 | 28.3 | 0.0 |
| Developer Experience | 72.4 | 30.7 | 95.3 | 86.1 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency p50 (s) | 65.76 | 107.87 | 146.93 | 300.00 |
| Latency p95 (s) | 147.00 | 261.44 | 211.96 | 300.00 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Actual Agents Avg | 2.300 | 1.700 | 2 | 0.100 |
| Agent Coverage Avg | 0.950 | 0.833 | 0.800 | 0.050 |
| Coordination Avg Agent Coverage | 0.929 | 0.762 | 0.714 | 0.071 |
| Coordination Avg Grounded Hop Coverage | 0.893 | 0.750 | 0 | 0.048 |
| Coordination Avg Hop Coverage | 0.893 | 0.750 | 0 | 0.095 |
| Coordination Avg Tool Coverage | 0.929 | 0.762 | 0.714 | 0.071 |
| Coordination Points Avg | 2.200 | 2.200 | 2.200 | 2.200 |
| Coordination Questions | 7 | 7 | 7 | 7 |
| Coordination Success Avg | 0.500 | 0.500 | 0 | 0 |
| Coordination Success Rate | 0.714 | 0.714 | 0 | 0 |
| Easy Avg Hop Coverage | 1 | 0.667 | 0 | 0 |
| Easy Questions | 3 | 3 | 3 | 3 |
| Grounded Hop Coverage Avg | 0.925 | 0.725 | 0 | 0.033 |
| Has Tool Trace Avg | 1 | 0.900 | 1 | 0.100 |
| Hop Coverage Avg | 0.925 | 0.725 | 0 | 0.067 |
| Is Coordination Avg | 0.700 | 0.700 | 0.700 | 0.700 |
| Is Easy Avg | 0.300 | 0.300 | 0.300 | 0.300 |
| Matched Hops Avg | 2.600 | 1.900 | 0 | 0.200 |
| Matched Tools Avg | 2 | 1.600 | 1.600 | 0.100 |
| Required Agents Avg | 2.100 | 2.100 | 2.100 | 2.100 |
| Required Hops Avg | 2.800 | 2.800 | 2.800 | 2.800 |
| Required Tools Count Avg | 2.100 | 2.100 | 2.100 | 2.100 |
| Tool Calls Reported Avg | 14.200 | 8.800 | 19.900 | 0.100 |
| Tool Coverage Avg | 0.950 | 0.833 | 0.800 | 0.050 |
| Tool Trace Rate | 1 | 0.900 | 1 | 0.100 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Source Lines (SLOC) | 257 | 313 | 294 | 237 |
| Comment Ratio | 2% | 3% | 5% | 2% |
| Avg Cyclomatic Complexity | 2.1 | 3.1 | 2.3 | 2.3 |
| Max Cyclomatic Complexity | 9 | 10 | 11 | 8 |
| Complexity Grade | A | A | A | A |
| Maintainability Index | 40.3 | 39.4 | 45.1 | 43.5 |
| Maintainability Grade | A | A | A | A |
| Halstead Volume | 653 | 339 | 299 | 331 |
| Halstead Difficulty | 4.3 | 6.9 | 5.1 | 4.7 |
| Halstead Bugs (est.) | 0.22 | 0.11 | 0.10 | 0.11 |
| Total Imports | 8 | 13 | 10 | 9 |
| Framework Imports | 1 | 6 | 1 | 0 |
| Classes | 3 | 1 | 8 | 6 |
| Functions | 19 | 24 | 18 | 12 |
| Type Annotation Coverage | 100% | 92% | 100% | 100% |

## Per-Question Results

### q1: What services run on the prod-us-east-1 cluster and what are their tiers?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 24.75 | 20.04 | 149.75 | 300.00 |
| Tokens | 5,449 | 3,407 | 0 | 0 |
| Correctness | 5 | 5 | 1 | 0 |
| Completeness | 5 | 5 | 1 | 0 |
| Faithfulness | 5 | 4 | 1 | 0 |
| Retrieval Prec | 0.25 | 0.50 | 0.11 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 1 | 1 | 2 | 0 |
| Agent Coverage | 1 | 1 | 1 | 0 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 | 0 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 | 0 |
| Matched Tools | 1 | 1 | 1 | 0 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 2 | 1 | 18 | 0 |
| Tool Coverage | 1 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Summary for cluster prod-us-east-1

Services (name — service_id — tier — version — last_deploy_at)
- api-gateway — SVC-001 — critical — api-gw:v3.1.0 — 2026-02-08T10:00:00Z
- auth-service — SVC-002 — critical — auth:v2.4.1-rc3 — 2026-02-10T16:30:00Z
- payment-service — SVC-003 — critical — payment:v...
- **LangGraph**: Summary (evidence)
- Query used:
  SELECT s.name AS service_name, s.tier
  FROM services s
  JOIN clusters c ON s.cluster_id = c.cluster_id
  WHERE c.name = 'prod-us-east-1';
- Result: 4 rows
  - api-gateway — critical
  - auth-service — critical
  - payment-service — critical
  - user-profile — sta...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 48.78 | 64.64 | 177.75 | 300.00 |
| Tokens | 18,098 | 25,673 | 0 | 0 |
| Correctness | 5 | 1 | 1 | 0 |
| Completeness | 4 | 1 | 1 | 0 |
| Faithfulness | 5 | 1 | 1 | 0 |
| Retrieval Prec | 0.20 | 1.00 | 0.20 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 2 | 1 | 1 | 0 |
| Agent Coverage | 1 | 1 | 1 | 0 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 0 | 0 | 0 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 0 | 0 | 0 |
| Matched Tools | 1 | 1 | 1 | 0 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 6 | 2 | 14 | 0 |
| Tool Coverage | 1 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer
- Yes — there is 1 open Critical vulnerability.

Details (evidence)
- Identifier: SCAN-201 (scan_id used as vulnerability id)
- CVE: CVE-2025-31337
- Description: Remote code execution in container base image
- Affected resource: service SVC-004
- Discovered at: 2026-02-08T06:00:00Z (UT...
- **LangGraph**: I'll check the vulnerability management policy to cite remediation SLA for critical issues.
To=functions.query_security  ConversationsUnavailable-user-json
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 50.85 | 37.69 | 140.14 | 300.00 |
| Tokens | 13,059 | 9,331 | 0 | 0 |
| Correctness | 5 | 5 | 1 | 0 |
| Completeness | 5 | 5 | 1 | 0 |
| Faithfulness | 4 | 5 | 1 | 0 |
| Retrieval Prec | 0.33 | 1.00 | 0.33 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 1 | 1 | 1 | 0 |
| Agent Coverage | 1 | 1 | 1 | 0 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 | 0 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 | 0 |
| Matched Tools | 1 | 1 | 1 | 0 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 5 | 2 | 12 | 0 |
| Tool Coverage | 1 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer — official escalation triggers (Sev2 → Sev1)
- Promote to Sev1 immediately if ANY of the following are true:
  1. Cascading impact detected — the affected service has downstream dependents that are also degraded.  
  2. Incident remains in "investigating" status for > 60 minutes without...
- **LangGraph**: Summary (direct policy reference)
- The runbook states: “A Sev2 incident MUST be escalated to Sev1 if ANY of the following are true” (incident_response_runbook.md — “Escalation Triggers: Sev2 to Sev1”). The listed triggers are:

Escalation triggers (exact, policy-backed)
1. Cascading impact detected...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 180.05 | 122.72 | 134.53 | 300.00 |
| Tokens | 47,168 | 109,569 | 0 | 0 |
| Correctness | 5 | 3 | 1 | 0 |
| Completeness | 5 | 4 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 0.18 | 0.25 | 0.17 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 3 | 2 | 3 | 0 |
| Agent Coverage | 1 | 1 | 1 | 0 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 1 | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 | 0 |
| Matched Tools | 2 | 2 | 2 | 0 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 23 | 10 | 30 | 0 |
| Tool Coverage | 1 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: No — the most recent auth-service deploy (DEP-102, 2026-02-10T16:30:00Z) was not compliant with NimbusOps change management policy based on the evidence available.

Evidence
- Deploy record (in recent_deploys):
  - deploy_id: DEP-102
  - service: auth-service (SVC-002)
  - deployed_at:...
- **LangGraph**: Verdict: Non‑compliant.

Key evidence
- Service: auth-service (SVC-002), tier = critical. (service_catalog.md; services table)
- Deploy record (recent_deploys):
  - deploy_id: DEP-102
  - deployed_at: 2026-02-10T16:30:00Z
  - deployed_by: bob@nimbusops.io
  - change_ticket: NULL (no CHG referenced)
...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 88.93 | 184.77 | 150.28 | 300.00 |
| Tokens | 21,546 | 205,565 | 0 | 0 |
| Correctness | 5 | 5 | 1 | 0 |
| Completeness | 4 | 5 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 0.14 | 0.18 | 0.18 | 0.00 |
| Retrieval Recall | 0.50 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 2 | 3 | 3 | 0 |
| Agent Coverage | 0.500 | 1 | 1 | 0 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 0 | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.500 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 0.500 | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 1 | 2 | 0 | 0 |
| Matched Tools | 1 | 2 | 2 | 0 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 2 | 2 | 2 | 2 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 13 | 18 | 30 | 0 |
| Tool Coverage | 0.500 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: No — the FW-404 change on prod-eu-west-1 was not recorded as an authorized, human-approved change.

Evidence (from our systems)
- Cluster mapping: CL-002 = prod-eu-west-1 (region eu-west-1, environment production).
- Firewall rule record:
  - rule_id: FW-404, cluster_id: CL-002 (prod-e...
- **LangGraph**: Short answer: No — FW-404 on prod-eu-west-1 was not properly authorized based on the evidence in our systems and the applicable policies.

Evidence (facts from our systems)
- Firewall rule record
  - rule_id: FW-404, cluster_id: CL-002, direction: ingress, source_cidr: 198.51.100.0/24, dest_port: 80...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 49.10 | 106.09 | 145.22 | 148.15 |
| Tokens | 18,199 | 51,836 | 0 | 2,516,016 |
| Correctness | 5 | 5 | 1 | 2 |
| Completeness | 4 | 5 | 1 | 2 |
| Faithfulness | 5 | 4 | 1 | 2 |
| Retrieval Prec | 0.40 | 0.40 | 0.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 0.50 |
| Actual Agents | 2 | 2 | 1 | 1 |
| Agent Coverage | 1 | 1 | 0 | 0.500 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 1 | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 0.333 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 | 0.667 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 | 2 |
| Matched Tools | 2 | 2 | 0 | 1 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 9 | 8 | 10 | 1 |
| Tool Coverage | 1 | 1 | 0 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: None — there are no services that appear in both sets.

Evidence
- Open critical/high vulnerabilities (from vulnerability_scans)
  - service_id: SVC-004 (order-service)
    - scan_id: SCAN-201, severity: critical, status: open, detected_at: 2026-02-08T06:00:00Z, CVE: CVE-2025-31337 (de...
- **LangGraph**: Direct answer
- None. No service in the current data set has both (a) an open critical or high vulnerability AND (b) a recent deploy record that lacks a change ticket.

Evidence (explicit data points)
- Open critical / high vulnerabilities (vulnerability_scans):
  - SVC-004 — CVE-2025-31337 — severi...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Summary conclusion
- There are no services that meet both criteria (A) open CRITICAL or HIGH vulnerabilities AND (B) recent deploys (last 7 days) without valid change tickets.
- Evidence:
  - Security query: zero open CRITICAL/HIGH vulnerabilities (raw result set empty).
  - Infrastructure query: 9 ...

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 92.08 | 109.66 | 137.01 | 300.00 |
| Tokens | 49,288 | 83,587 | 0 | 0 |
| Correctness | 5 | 5 | 1 | 0 |
| Completeness | 5 | 4 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 0.50 | 0.50 | 0.67 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.67 | 0.00 |
| Actual Agents | 3 | 3 | 1 | 0 |
| Agent Coverage | 1 | 1 | 0.333 | 0 |
| Coordination Points | 4 | 4 | 4 | 4 |
| Coordination Success | 0 | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.750 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 0.750 | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 4 | 0 | 0 |
| Matched Tools | 3 | 3 | 1 | 0 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 24 | 18 | 9 | 0 |
| Tool Coverage | 1 | 1 | 0.333 | 0 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: a performance regression introduced by the auth-service deploy (auth:v2.4.1-rc3 at 2026-02-10T16:30) that increased auth p99 latency (~120ms → ~8200ms) and caused synchronous auth calls from payment-service to time out/return 503s.
- Was incident response proper? Pa...
- **LangGraph**: Summary (short)
- Likely root cause: a latency regression introduced by the auth-service deploy (auth:v2.4.1-rc3, DEP-102, deployed 2026-02-10T16:30:00Z) caused auth p99 to spike (~8200ms vs baseline 120ms). Because payment-service calls auth synchronously, payment returned 503s (INC-4001).
- Incide...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 106.62 | 300.00 | 148.65 | 300.00 |
| Tokens | 72,722 | 0 | 0 | 0 |
| Correctness | 5 | 0 | 1 | 0 |
| Completeness | 5 | 0 | 1 | 0 |
| Faithfulness | 5 | 0 | 1 | 0 |
| Retrieval Prec | 0.54 | 0.00 | 0.54 | 0.00 |
| Retrieval Recall | 1.00 | 0.00 | 1.00 | 0.00 |
| Actual Agents | 3 | 0 | 3 | 0 |
| Agent Coverage | 1 | 0 | 1 | 0 |
| Coordination Points | 5 | 5 | 5 | 5 |
| Coordination Success | 1 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0 | 0 | 0 |
| Has Tool Trace | 1 | 0 | 1 | 0 |
| Hop Coverage | 1 | 0 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 5 | 0 | 0 | 0 |
| Matched Tools | 3 | 0 | 3 | 0 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 5 | 5 | 5 | 5 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 24 | 0 | 30 | 0 |
| Tool Coverage | 1 | 0 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Summary (short)
- Probable root cause: a production firewall change (FW-404) opened order-service (SVC-004) port 8083 to an external CIDR (198.51.100.0/24) at 2026-02-10T12:00:00Z, combined with an open, unremediated critical RCE (SCAN-201 / CVE-2025-31337) on order-service. External scanner/attack ...
- **LangGraph**: Query timed out before producing an answer.
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 70.15 | 91.36 | 239.94 | 300.00 |
| Tokens | 28,572 | 41,254 | 0 | 0 |
| Correctness | 4 | 2 | 1 | 0 |
| Completeness | 3 | 2 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 0.50 | 1.00 | 0.50 | 0.00 |
| Retrieval Recall | 0.86 | 0.43 | 0.71 | 0.00 |
| Actual Agents | 3 | 1 | 2 | 0 |
| Agent Coverage | 1 | 0.333 | 0.667 | 0 |
| Coordination Points | 4 | 4 | 4 | 4 |
| Coordination Success | 1 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0.250 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 0.250 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 4 | 1 | 0 | 0 |
| Matched Tools | 3 | 1 | 2 | 0 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 17 | 9 | 20 | 0 |
| Tool Coverage | 1 | 0.333 | 0.667 | 0 |

**Answers:**

- **Pydantic AI**: Short answer (top-line)
- Sequence (condensed): 1) Triage & escalate → 2) Contain (block traffic / isolate) → 3) Preserve evidence & investigate → 4) Remediate (rollback or patch + deploy) → 5) Verify & monitor → 6) Document & post‑mortem.
- Who must approve: Incident Commander (for emergency action...
- **LangGraph**: Below is a single, actionable remediation sequence for INC-4002 plus the exact approvers and policy citations you must meet. I don’t have an INC-4002-specific entry in the runbooks, so this is the required process based on our Incident Response, Change Management and Security & Compliance policies. ...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 61.37 | 214.31 | 136.71 | 300.00 |
| Tokens | 47,980 | 412,497 | 0 | 0 |
| Correctness | 5 | 5 | 1 | 0 |
| Completeness | 4 | 5 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 0.46 | 0.46 | 0.55 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 0.00 |
| Actual Agents | 3 | 3 | 3 | 0 |
| Agent Coverage | 1 | 1 | 1 | 0 |
| Coordination Points | 3 | 3 | 3 | 3 |
| Coordination Success | 1 | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 4 | 4 | 0 | 0 |
| Matched Tools | 3 | 3 | 3 | 0 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 19 | 20 | 26 | 0 |
| Tool Coverage | 1 | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — escalate INC-4002 from sev2 to sev1 now.

Why (policy triggers + evidence)
- Suspected active compromise (runbook escalation trigger):
  - Evidence: multiple high-anomaly access-log entries to SVC-004 from 198.51.100.0/24 in the 25 minutes before the incident open (LOG-301/302/30...
- **LangGraph**: Decision: Yes — escalate INC-4002 from sev2 to sev1 now.

Why (evidence → policy mapping)
- Investigating > 60 minutes:
  - Evidence: INC-4002 opened 2026-02-10T14:30:00Z; status = investigating; identified_at = null; timeline entries continue through 2026-02-10T16:00:00Z (≈1.5 hours).  
  - Policy:...
- **smolagents**: Agent timed out or was interrupted before producing an answer.
- **CrewAI**: Query timed out before producing an answer.
