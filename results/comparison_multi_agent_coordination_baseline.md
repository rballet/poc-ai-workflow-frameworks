# Framework Comparison Report

Generated: 2026-02-12 13:32 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: baseline
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 31.95 | 28.97 | 14.59 |
| Total Tokens | 70,235 | 60,995 | 33,100 |
| Est. Cost (USD) | $0.0688 | $0.0636 | $0.0317 |
| Avg Correctness (1-5) | 3.6 | 3.2 | 1.4 |
| Avg Completeness (1-5) | 3.3 | 2.7 | 1.4 |
| Avg Faithfulness (1-5) | 4.9 | 4.8 | 2.1 |
| Avg Retrieval Precision | 0.61 | 0.56 | 0.15 |
| Avg Retrieval Recall | 0.63 | 0.56 | 0.11 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Capability | 78.7 | 71.3 | 32.7 |
| Efficiency | 0.0 | 5.8 | 33.3 |
| Developer Experience | N/A | N/A | N/A |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency p50 (s) | 27.75 | 30.16 | 14.35 |
| Latency p95 (s) | 51.04 | 39.38 | 24.36 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Actual Agents Avg | 2.200 | 2.100 | 1.300 |
| Agent Coverage Avg | 0.933 | 0.933 | 0.700 |
| Coordination Avg Agent Coverage | 0.905 | 0.905 | 0.571 |
| Coordination Avg Grounded Hop Coverage | 0.390 | 0.243 | 0 |
| Coordination Avg Hop Coverage | 0.817 | 0.545 | 0.048 |
| Coordination Avg Tool Coverage | 0.905 | 0.905 | 0.571 |
| Coordination Points Avg | 2.200 | 2.200 | 2.200 |
| Coordination Questions | 7 | 7 | 7 |
| Coordination Success Avg | 0.300 | 0.100 | 0 |
| Coordination Success Rate | 0.429 | 0.143 | 0 |
| Easy Avg Hop Coverage | 1 | 1 | 0.333 |
| Easy Questions | 3 | 3 | 3 |
| Grounded Hop Coverage Avg | 0.573 | 0.470 | 0.100 |
| Has Tool Trace Avg | 1 | 1 | 1 |
| Hop Coverage Avg | 0.872 | 0.682 | 0.133 |
| Is Coordination Avg | 0.700 | 0.700 | 0.700 |
| Is Easy Avg | 0.300 | 0.300 | 0.300 |
| Matched Hops Avg | 2.400 | 1.600 | 0.200 |
| Matched Tools Avg | 1.900 | 1.900 | 1.300 |
| Required Agents Avg | 2.100 | 2.100 | 2.100 |
| Required Hops Avg | 2.800 | 2.800 | 2.800 |
| Required Tools Count Avg | 2.100 | 2.100 | 2.100 |
| Tool Calls Reported Avg | 2.900 | 2.800 | 1.300 |
| Tool Coverage Avg | 0.933 | 0.933 | 0.700 |
| Tool Trace Rate | 1 | 1 | 1 |

## Per-Question Results

### q1: What services run on the prod-us-east-1 cluster and what are their tiers?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 11.29 | 6.94 | 15.91 |
| Tokens | 2,561 | 1,547 | 3,324 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Actual Agents | 1 | 1 | 1 |
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
| Tool Calls Reported | 2 | 1 | 1 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: I queried the infrastructure service registry for cluster "prod-us-east-1". Services running there and their tiers:

- api-gateway (service_id: SVC-001) — critical  
- auth-service (service_id: SVC-002) — critical  
- payment-service (service_id: SVC-003) — critical  
- user-profile (service_id: SVC...
- **LangGraph**: I queried the infrastructure inventory for cluster "prod-us-east-1". Services running there and their tiers:

- api-gateway (SVC-001) — critical  
- auth-service (SVC-002) — critical  
- payment-service (SVC-003) — critical  
- user-profile (SVC-008) — standard

Source: infrastructure services table...
- **smolagents**: Calling tool to run the query for services on prod-us-east-1...

[Tool call]
function: query_infrastructure
arguments:
{
  "query": "SELECT s.service_id AS service_id, s.name AS service_name, s.tier AS tier FROM services s JOIN clusters c ON s.cluster_id = c.cluster_id WHERE c.name = 'prod-us-east-1...

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 24.35 | 22.81 | 9.28 |
| Tokens | 5,827 | 6,416 | 2,469 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 4 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 1.00 | 0.50 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
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

- **Pydantic AI**: Short answer
- Yes. There is 1 open critical vulnerability:
  - Scan ID: SCAN-201
  - Service: SVC-004
  - CVE: CVE-2025-31337
  - Description: Remote code execution in container base image
  - Scanned at: 2026-02-08T06:00:00Z
  - Status: open
  - Remediation deadline: 2026-02-09T06:00:00Z — this de...
- **LangGraph**: Short answer: Yes — there is one open critical vulnerability.

Details (from vulnerability_scans):
- scan_id: SCAN-201
- service_id: SVC-004
- cve_id: CVE-2025-31337
- description: Remote code execution in container base image
- severity: critical
- status: open
- detected/scanned_at: 2026-02-08T06:...
- **smolagents**: Calling tool to retrieve critical vulnerabilities (excluding resolved/closed/mitigated)...

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 29.15 | 29.41 | 7.70 |
| Tokens | 8,009 | 5,577 | 2,730 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.50 | 0.50 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Actual Agents | 3 | 2 | 1 |
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
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer — the runbook lists four explicit triggers. Escalate a Sev2 to Sev1 if ANY of the following are true:

1. Cascading impact detected — the affected service has downstream dependents that are also degraded.  
2. The incident remains in "investigating" status for more than 60 minutes witho...
- **LangGraph**: Short answer — per our incident response runbook, escalate a Sev2 to Sev1 immediately if ANY of the following are true:

1. Cascading impact detected — the affected service has downstream dependents that are also degraded or failing.  
2. Investigation remains in “investigating” for > 60 minutes wit...
- **smolagents**: Per the incident response runbook, a Sev2 MUST be promoted to Sev1 if ANY of the following escalation triggers are met:

1. Cascading impact detected — the affected service has downstream dependents that are also degraded.  
2. The incident remains in "investigating" status for more than 60 minutes ...

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 38.29 | 28.97 | 8.76 |
| Tokens | 7,539 | 6,800 | 2,656 |
| Correctness | 3 | 2 | 1 |
| Completeness | 2 | 2 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.33 | 0.00 |
| Retrieval Recall | 1.00 | 0.50 | 0.00 |
| Actual Agents | 2 | 2 | 1 |
| Agent Coverage | 1 | 1 | 0.500 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 1 | 1 | 0 |
| Grounded Hop Coverage | 1 | 0.667 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 3 | 0 |
| Matched Tools | 2 | 2 | 1 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 1 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: No — based on available evidence the most recent deploy of auth-service (DEP-102) appears non‑compliant with the change management policy.

Evidence found
- recent_deploys row for auth-service (DEP-102)
  - deployed_at: 2026-02-10T16:30:00Z
  - deployed_by: bob@nimbusops.io
  - change_...
- **LangGraph**: Short answer: I cannot determine compliance with the change-management policy from the data I was able to fetch. I did retrieve some relevant facts and the policy text, but the critical deployment metadata needed to decide compliance is missing.

What I did fetch
- Service record:
  - service_id: SV...
- **smolagents**: Calling tools:
[{'id': 'call_1', 'type': 'function', 'function': {'name': 'query_infrastructure', 'arguments': {'query': "SELECT * FROM services WHERE name = 'auth-service';"}}}]

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 26.00 | 39.74 | 14.15 |
| Tokens | 4,411 | 8,655 | 2,940 |
| Correctness | 2 | 2 | 1 |
| Completeness | 2 | 2 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.00 |
| Actual Agents | 2 | 2 | 1 |
| Agent Coverage | 1 | 1 | 0.500 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.500 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 2 | 2 | 1 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 2 | 2 | 2 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 1 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: I can’t confirm whether FW-404 was properly authorized with the data I retrieved. I was able to fetch the firewall/change-management policy (which requires a CHG ticket and security approval for production changes), but I could not retrieve the firewall rule record or the access log en...
- **LangGraph**: Short answer: I cannot confirm whether FW-404 on prod-eu-west-1 was properly authorized with the information available. The change-management and security runbooks require an approved change ticket plus security approval for production changes (or explicit incident-commander authorization + retroact...
- **smolagents**: Calling tools:
[{"id":"call_1","type":"function","function":{"name":"query_security","arguments":{"query":"SELECT rule_id, cluster_id, direction, source_cidr, dest_port, protocol, action, last_modified_at, modified_by FROM firewall_rules WHERE rule_id = 'FW-404';"}}}]

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 26.36 | 26.00 | 22.82 |
| Tokens | 5,152 | 4,477 | 4,340 |
| Correctness | 3 | 3 | 1 |
| Completeness | 3 | 2 | 1 |
| Faithfulness | 5 | 3 | 4 |
| Retrieval Prec | 0.50 | 1.00 | 0.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.00 |
| Actual Agents | 2 | 2 | 2 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0.333 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 1 |
| Matched Tools | 2 | 2 | 2 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 2 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer
- I can confirm two services have open critical/high vulnerabilities: 
  - SVC-003 — payment-service (1 high, open)  
  - SVC-004 — order-service (1 critical, open)  
- I cannot yet confirm whether those same services have recent deploys without change tickets because my attempt to fetc...
- **LangGraph**: Answer: None — there are no services that match both criteria.

Evidence:
- I queried vulnerability_scans for open Critical or High findings (severity IN ('Critical','High') AND LOWER(status)='open'). That returned 0 rows (no open Critical/High vulnerabilities in the table).
- Because a service must...
- **smolagents**: I don’t yet have the query results — I need to run a DB query to get them. Below is the correct single SQL to return services that have both (A) at least one open vulnerability with severity critical or high and (B) at least one recent deploy record with no change ticket. It uses the actual column n...

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 38.15 | 34.11 | 19.96 |
| Tokens | 10,639 | 7,079 | 3,951 |
| Correctness | 5 | 1 | 1 |
| Completeness | 4 | 1 | 1 |
| Faithfulness | 5 | 5 | 2 |
| Retrieval Prec | 0.80 | 0.50 | 0.00 |
| Retrieval Recall | 0.67 | 0.17 | 0.00 |
| Actual Agents | 2 | 3 | 1 |
| Agent Coverage | 0.667 | 1 | 0.333 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.750 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.750 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 0 | 0 |
| Matched Tools | 2 | 3 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.667 | 1 | 0.333 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: a performance/regression in auth-service caused by the 16:30 deploy (v2.4.1-rc3) that increased p99 latency (~8.2s vs ~120ms baseline), causing payment-service (which synchronously depends on auth) to return 503s.
- Was response proper? Partially. The incident was d...
- **LangGraph**: Short answer
- I cannot definitively say the root cause of INC-4001 or whether the runbook was followed because I was unable to retrieve any incident-specific records (incidents row, timeline, deploys, scans, or logs) before the tool budget was exhausted.
- Based on common failure modes and our runb...
- **smolagents**: I can run up to 3 read-only queries against the incident DB to determine the root cause and evaluate the response. Plan:

1) Fetch the INC-4001 incident record (incidents table).
2) Fetch the incident timeline entries (incident_timeline) ordered by timestamp.
3) Fetch recent deploys for the affected...

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 59.12 | 38.94 | 25.62 |
| Tokens | 9,027 | 6,417 | 5,529 |
| Correctness | 1 | 2 | 1 |
| Completeness | 2 | 2 | 1 |
| Faithfulness | 5 | 5 | 4 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 0.14 | 0.14 | 0.14 |
| Actual Agents | 3 | 3 | 3 |
| Agent Coverage | 1 | 1 | 1 |
| Coordination Points | 5 | 5 | 5 |
| Coordination Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.400 | 0.200 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.800 | 0.400 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 4 | 2 | 0 |
| Matched Tools | 3 | 3 | 3 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 5 | 5 | 5 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 3 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Summary / constraints
- I attempted to fetch incident and security data but the tool call budget was exhausted before I could retrieve INC-4002’s records, timeline, access logs, vulnerability scans, firewall changes, and recent deploy history.
- I was able to retrieve relevant runbook/policy excerpt...
- **LangGraph**: Short answer / status
- I attempted to pull incident and security evidence but the automated queries failed (tool errors). I do not have the incident row, timeline entries, access log slices, vulnerability scan results or firewall-change history for INC-4002 available to me in this session, so I can...
- **smolagents**: I'll query the incident, timeline, service, cluster, recent deploys, access logs, vulnerability scans, and firewall rules for INC-4002 (two read-only queries).
Calling tools:
1/2: query_infrastructure
Query:
SELECT * FROM incidents WHERE incident_id='INC-4002';
SELECT * FROM incident_timeline WHERE ...

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 25.58 | 30.91 | 7.12 |
| Tokens | 9,413 | 7,409 | 2,414 |
| Correctness | 4 | 3 | 1 |
| Completeness | 3 | 2 | 1 |
| Faithfulness | 4 | 5 | 1 |
| Retrieval Prec | 0.33 | 0.75 | 0.00 |
| Retrieval Recall | 0.14 | 0.43 | 0.00 |
| Actual Agents | 2 | 2 | 1 |
| Agent Coverage | 0.667 | 0.667 | 0.333 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0.250 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 4 | 2 | 0 |
| Matched Tools | 2 | 2 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 0.667 | 0.667 | 0.333 |

**Answers:**

- **Pydantic AI**: Summary of evidence (from INC-4002 timeline)
- p95 latency on order-service (SVC-004) spiked to 4500ms in eu-west-1 (monitoring alert).
- Security detected anomalous traffic to SVC-004: source 198.51.100.0/24, high anomaly scores.
- Firewall rule FW-404 opened port 8083 to 198.51.100.0/24 by bot-sca...
- **LangGraph**: Summary (grounded to runbook + incident record)
- INC-4002: "order-service degraded performance in eu-west-1" — current status investigating, severity = sev2, incident commander = dave@nimbusops.io.
- Relevant policies:
  - Emergency change process: the incident commander must explicitly authorize a...
- **smolagents**: Calling tools:
[{"id":"call_1","type":"function","function":{"name":"query_infrastructure","arguments":{"query":"SELECT incident_id, title, severity, status, affected_service_id, opened_at, identified_at, resolved_at, commander, root_cause FROM incidents WHERE incident_id = 'INC-4002' LIMIT 1;"}}}]

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 41.18 | 31.87 | 14.55 |
| Tokens | 7,657 | 6,618 | 2,747 |
| Correctness | 3 | 4 | 1 |
| Completeness | 2 | 2 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 1.00 | 0.50 | 0.00 |
| Retrieval Recall | 0.33 | 0.33 | 0.00 |
| Actual Agents | 3 | 2 | 1 |
| Agent Coverage | 1 | 0.667 | 0.333 |
| Coordination Points | 3 | 3 | 3 |
| Coordination Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.250 | 0.250 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 0.750 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 4 | 3 | 0 |
| Matched Tools | 3 | 2 | 1 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 |
| Tool Coverage | 1 | 0.667 | 0.333 |

**Answers:**

- **Pydantic AI**: Short answer: I cannot definitively say “yes” or “no” because I don’t have the incident data (INC-4002 row, timeline, service, access logs, dependency info). Based on NimbusOps policy, escalation to Sev1 is required if any of several specific triggers are met — I list them below and give the exact e...
- **LangGraph**: Short answer: Yes — escalate INC-4002 from sev2 to sev1.

Evidence:
- Incident record (infrastructure lookup):
  - incident_id: INC-4002
  - title: "order-service degraded performance in eu-west-1"
  - severity: sev2
  - status: investigating
  - opened_at: 2026-02-10T14:30:00Z
  - identified_at: NU...
- **smolagents**: Calling tool to fetch the incident record (1/3)...
