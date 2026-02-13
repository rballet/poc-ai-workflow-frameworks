# Framework Comparison Report

Generated: 2026-02-12 22:33 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: baseline
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Latency (s) | 31.08 | 31.26 | 10.64 | 69.79 |
| Total Tokens | 62,582 | 71,164 | 28,742 | 519,170 |
| Est. Cost (USD) | $0.0709 | $0.0727 | $0.0247 | $0.6110 |
| Avg Correctness (1-5) | 3.7 | 3.6 | 1.4 | 2.6 |
| Avg Completeness (1-5) | 3.3 | 3.4 | 1.4 | 2.2 |
| Avg Faithfulness (1-5) | 4.7 | 4.8 | 1.3 | 3.1 |
| Avg Retrieval Precision | 0.80 | 0.70 | 0.20 | 0.60 |
| Avg Retrieval Recall | 0.64 | 0.70 | 0.11 | 0.55 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Capability | 78.0 | 78.7 | 27.3 | 52.7 |
| Efficiency | 27.2 | 27.0 | 33.3 | 0.0 |
| Developer Experience | 72.4 | 30.7 | 95.3 | 86.1 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency p50 (s) | 34.08 | 29.65 | 10.03 | 68.61 |
| Latency p95 (s) | 46.62 | 46.36 | 17.84 | 114.88 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Actual Agents Avg | 1.700 | 1.800 | 1.100 | 1.500 |
| Agent Coverage Avg | 0.783 | 0.800 | 0.633 | 0.700 |
| Coordination Avg Agent Coverage | 0.690 | 0.714 | 0.476 | 0.571 |
| Coordination Avg Grounded Hop Coverage | 0.357 | 0.476 | 0 | 0.274 |
| Coordination Avg Hop Coverage | 0.669 | 0.795 | 0.048 | 0.393 |
| Coordination Avg Tool Coverage | 0.690 | 0.714 | 0.476 | 0.571 |
| Coordination Points Avg | 2.200 | 2.200 | 2.200 | 2.200 |
| Coordination Questions | 7 | 7 | 7 | 7 |
| Coordination Success Avg | 0 | 0.200 | 0 | 0 |
| Coordination Success Rate | 0 | 0.286 | 0 | 0 |
| Easy Avg Hop Coverage | 1 | 1 | 0.333 | 0.667 |
| Easy Questions | 3 | 3 | 3 | 3 |
| Grounded Hop Coverage Avg | 0.550 | 0.633 | 0.100 | 0.392 |
| Has Tool Trace Avg | 1 | 1 | 1 | 0.900 |
| Hop Coverage Avg | 0.768 | 0.857 | 0.133 | 0.475 |
| Is Coordination Avg | 0.700 | 0.700 | 0.700 | 0.700 |
| Is Easy Avg | 0.300 | 0.300 | 0.300 | 0.300 |
| Matched Hops Avg | 2 | 2.200 | 0.200 | 1.100 |
| Matched Tools Avg | 1.500 | 1.500 | 1.100 | 1.300 |
| Required Agents Avg | 2.100 | 2.100 | 2.100 | 2.100 |
| Required Hops Avg | 2.800 | 2.800 | 2.800 | 2.800 |
| Required Tools Count Avg | 2.100 | 2.100 | 2.100 | 2.100 |
| Tool Calls Reported Avg | 2.600 | 2.900 | 1.100 | 2.600 |
| Tool Coverage Avg | 0.783 | 0.800 | 0.633 | 0.700 |
| Tool Trace Rate | 1 | 1 | 1 | 0.900 |

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
| Latency (s) | 5.69 | 8.46 | 10.38 | 15.93 |
| Tokens | 1,615 | 2,529 | 2,671 | 3,879 |
| Correctness | 5 | 5 | 1 | 5 |
| Completeness | 5 | 5 | 1 | 5 |
| Faithfulness | 5 | 5 | 1 | 5 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 | 0.50 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Actual Agents | 1 | 1 | 1 | 1 |
| Agent Coverage | 1 | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 1 | 2 | 1 | 2 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: From the infrastructure inventory, these services run on cluster prod-us-east-1:

- api-gateway (SVC-001) — tier: critical  
- auth-service (SVC-002) — tier: critical  
- payment-service (SVC-003) — tier: critical  
- user-profile (SVC-008) — tier: standard

Source: infrastructure services table fil...
- **LangGraph**: I queried the infrastructure catalog for services tied to the cluster named "prod-us-east-1". Services running there and their tiers:

- SVC-001 — api-gateway — critical  
- SVC-002 — auth-service — critical  
- SVC-003 — payment-service — critical  
- SVC-008 — user-profile — standard

Would you li...
- **smolagents**: Calling tools:
[{'id': 'call_3qYbNxHkLr2mP0aZsE9fU1', 'type': 'function', 'function': {'name': 'query_infrastructure', 'arguments': {'query': "SELECT s.name AS service, s.tier FROM services s JOIN clusters c ON s.cluster_id = c.cluster_id WHERE c.name = 'prod-us-east-1';"}}}]
- **CrewAI**: Query result for services on cluster "prod-us-east-1" (from services JOIN clusters):

Row count: 4

Rows:
[
  {
    "service_name": "api-gateway",
    "tier": "critical"
  },
  {
    "service_name": "auth-service",
    "tier": "critical"
  },
  {
    "service_name": "payment-service",
    "tier": "c...

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 28.69 | 17.45 | 5.04 | 43.18 |
| Tokens | 7,844 | 5,252 | 2,198 | 12,029 |
| Correctness | 5 | 5 | 1 | 5 |
| Completeness | 5 | 4 | 1 | 4 |
| Faithfulness | 5 | 5 | 1 | 5 |
| Retrieval Prec | 0.50 | 1.00 | 0.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Actual Agents | 2 | 2 | 1 | 2 |
| Agent Coverage | 1 | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 | 1 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 | 1 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — there is 1 open critical vulnerability. Details below.

Open critical vulnerabilities
- Scan ID: SCAN-201
- Service: order-service (service_id SVC-004)
- CVE: CVE-2025-31337
- Description: Remote code execution in container base image
- Scan time: 2026-02-08T06:00:00Z
- Status: o...
- **LangGraph**: Short answer: Yes — there is one open critical vulnerability. It is overdue.

Evidence (from vulnerability_scans):
- scan_id: SCAN-201
- service_id: SVC-004
- scanned_at: 2026-02-08T06:00:00Z
- cve_id: CVE-2025-31337
- description: Remote code execution in container base image
- status: open
- remed...
- **smolagents**: Calling tool to fetch open critical vulnerabilities (1/3)...
- **CrewAI**: Open critical vulnerabilities (complete scan rows returned):

[
  {
    "scan_id": "SCAN-201",
    "service_id": "SVC-004",
    "scanned_at": "2026-02-08T06:00:00Z",
    "severity": "critical",
    "cve_id": "CVE-2025-31337",
    "description": "Remote code execution in container base image",
    "s...

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 13.28 | 24.83 | 9.21 | 57.49 |
| Tokens | 2,374 | 7,865 | 2,999 | 24,651 |
| Correctness | 5 | 5 | 5 | 1 |
| Completeness | 5 | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 4 | 1 |
| Retrieval Prec | 1.00 | 0.50 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Actual Agents | 1 | 2 | 1 | 1 |
| Agent Coverage | 1 | 1 | 1 | 1 |
| Coordination Points | 0 | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 0 |
| Is Coordination | 0 | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 1 | 0 |
| Matched Tools | 1 | 1 | 1 | 1 |
| Required Agents | 1 | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 | 1 |
| Tool Calls Reported | 1 | 3 | 1 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer: Escalate a Sev2 to Sev1 if ANY one of the listed triggers is true.

Escalation triggers (from the incident response runbook)
- Cascading impact detected — the affected service has downstream dependents that are also degraded.  
- Incident stuck in "investigating" for > 60 minutes witho...
- **LangGraph**: Short answer
- Per the incident response runbook, a Sev2 MUST be escalated to Sev1 if ANY of the following are true:
  1. Cascading impact detected — the affected service has downstream dependents that are also degraded.
  2. The incident remains in "investigating" status for more than 60 minutes wi...
- **smolagents**: Escalate a Sev2 to Sev1 if ANY of the following runbook triggers are true:

- Cascading impact detected — the affected service has downstream dependents that are also degraded.  
- Investigation stalled > 60 minutes — incident remains in "investigating" status for more than 60 minutes without identi...
- **CrewAI**: Thought: you should always think about what to do
Action: lookup_runbook
Action Input: {"query":"Escalation Triggers: Sev2 to Sev1 incident_response_runbook.md"}

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 41.17 | 42.97 | 10.56 | 53.14 |
| Tokens | 8,289 | 9,160 | 2,931 | 33,876 |
| Correctness | 3 | 3 | 1 | 3 |
| Completeness | 2 | 3 | 1 | 2 |
| Faithfulness | 5 | 3 | 1 | 3 |
| Retrieval Prec | 0.50 | 0.40 | 0.00 | 0.50 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 0.50 |
| Actual Agents | 2 | 2 | 1 | 1 |
| Agent Coverage | 1 | 1 | 0.500 | 0.500 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 0 | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 1 | 0 | 0.333 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 0.667 | 1 | 0 | 0.667 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 3 | 0 | 2 |
| Matched Tools | 2 | 2 | 1 | 1 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 1 | 1 | 0.500 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: Probably not compliant.

Evidence
- Recent deploy record (most recent):
  - deploy_id: DEP-102
  - service: auth-service
  - deployed_at: 2026-02-10T16:30:00Z (Tuesday)
  - deployed_by: bob@nimbusops.io
  - change_ticket: NULL
  - image_tag: auth:v2.4.1-rc3
  - rollback_available: true...
- **LangGraph**: Short answer: No — the most recent auth-service deploy (DEP-102) was not compliant with the change management policy.

Evidence
- Deploy record (infrastructure tables)
  - service: auth-service (tier = critical)
  - deploy_id: DEP-102
  - deployed_at: 2026-02-10T16:30:00Z
  - deployed_by: bob@nimbus...
- **smolagents**: I ran a query to fetch the most recent deploy for "auth-service" joined with the services table. Results and my assessment follow.

Query result (most recent deploy):
- service_id: 7
- name: auth-service
- team_owner: identity-team
- deploy_id: 4821
- deployed_at: 2026-02-11 18:23:45
- deployed_by: ...
- **CrewAI**: I reviewed the most recent deploy record for auth-service and the deploy metadata shows missing change-management artifacts. Complete deploy record from recent_deploys:
{
  "deploy_id": "DEP-102",
  "service_id": "SVC-002",
  "deployed_at": "2026-02-10T16:30:00Z",
  "deployed_by": "bob@nimbusops.io"...

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 35.60 | 44.22 | 19.06 | 108.61 |
| Tokens | 6,081 | 9,208 | 3,794 | 49,604 |
| Correctness | 3 | 5 | 1 | 3 |
| Completeness | 3 | 5 | 1 | 2 |
| Faithfulness | 5 | 5 | 1 | 5 |
| Retrieval Prec | 1.00 | 0.67 | 0.00 | 1.00 |
| Retrieval Recall | 0.50 | 1.00 | 0.00 | 0.50 |
| Actual Agents | 2 | 3 | 1 | 2 |
| Agent Coverage | 0.500 | 1 | 0.500 | 0.500 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 0 | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.500 | 1 | 0 | 0.500 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 0.500 | 1 | 0 | 0.500 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 1 | 2 | 0 | 1 |
| Matched Tools | 1 | 2 | 1 | 1 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 2 | 2 | 2 | 2 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 0.500 | 1 | 0.500 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: I cannot confirm it was properly authorized with the data available. Evidence shows an automated scanner made the change, but I’m missing change-control/approval and cluster-to-region mapping that are required to determine authorization.

What I found (grounded evidence)
- Firewall rul...
- **LangGraph**: Short answer: No — based on available evidence, FW-404 was not properly authorized and appears to be a compliance violation.

What I found (grounded evidence)
- Firewall rule record:
  - rule_id: FW-404
  - cluster_id: CL-002
  - direction: ingress
  - source_cidr: 198.51.100.0/24 (external, not in ...
- **smolagents**: Short answer: I cannot determine from the available schema whether "FW-404 on prod-eu-west-1" was properly authorized. The firewall_rules table does not include an environment field, so I can't reliably locate the rule by environment name. I can, however, give the exact queries and steps you should ...
- **CrewAI**: Evidence collected
- firewall_rules row (complete content returned by query_security):
[
  {
    "rule_id": "FW-404",
    "cluster_id": "CL-002",
    "direction": "ingress",
    "source_cidr": "198.51.100.0/24",
    "dest_port": 8083,
    "protocol": "tcp",
    "action": "allow",
    "last_modified_...

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 28.37 | 28.59 | 16.35 | 42.34 |
| Tokens | 5,350 | 5,078 | 3,560 | 58,831 |
| Correctness | 3 | 1 | 1 | 1 |
| Completeness | 2 | 1 | 1 | 1 |
| Faithfulness | 2 | 5 | 1 | 1 |
| Retrieval Prec | 1.00 | 1.00 | 0.00 | 0.50 |
| Retrieval Recall | 0.50 | 0.50 | 0.00 | 0.50 |
| Actual Agents | 2 | 2 | 2 | 2 |
| Agent Coverage | 1 | 1 | 1 | 1 |
| Coordination Points | 2 | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 0 | 0.333 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0.333 | 0.333 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 1 | 1 |
| Matched Tools | 2 | 2 | 2 | 2 |
| Required Agents | 2 | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 | 2 |
| Tool Calls Reported | 3 | 3 | 2 | 3 |
| Tool Coverage | 1 | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Short answer: None.

Evidence and reasoning
- I queried the vulnerability scanner data for any open Critical or High findings (severity IN ('Critical','High') and status not in closed/resolved/fixed). That query returned zero rows — i.e., there are no open Critical or High vulnerabilities recorded i...
- **LangGraph**: Short answer
- I found no services with open Critical or High vulnerabilities in vulnerability_scans (the query returned 0 rows).
- I could not complete the “recent deploys without change tickets” check because my tool-call budget was exhausted before I could fetch recent_deploys results. So I canno...
- **smolagents**: Calling the infra DB to find services meeting both conditions (open CRITICAL/HIGH vuln + recent deploy(s) with no change ticket)...
- **CrewAI**: Thought: check vulnerability_scans for open critical/high vulns for service SVC-002 (auth-service) — use remaining query.
Action: query_security
Action Input: {"query":"SELECT scan_id, service_id, scanned_at, severity, cve_id, description, status, remediation_deadline FROM vulnerability_scans WHERE ...

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 38.28 | 26.44 | 8.25 | 84.16 |
| Tokens | 8,272 | 7,860 | 2,633 | 73,093 |
| Correctness | 5 | 5 | 1 | 1 |
| Completeness | 4 | 5 | 1 | 1 |
| Faithfulness | 5 | 5 | 1 | 1 |
| Retrieval Prec | 1.00 | 0.75 | 0.00 | 0.00 |
| Retrieval Recall | 0.33 | 0.50 | 0.00 | 0.00 |
| Actual Agents | 1 | 1 | 1 | 2 |
| Agent Coverage | 0.333 | 0.333 | 0.333 | 0.667 |
| Coordination Points | 4 | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.250 | 0.500 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 0.750 | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 4 | 0 | 0 |
| Matched Tools | 1 | 1 | 1 | 2 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 0.333 | 0.333 | 0.333 | 0.667 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: a latency regression introduced by the auth-service deploy (v2.4.1-rc3) which caused auth calls to spike to p99 ≈ 8.2s; payment-service calls to auth timed out/fail and surfaced as 503s.
- Incident response: partially appropriate (fast detection and commander assign...
- **LangGraph**: Short answer
- Likely root cause: a latency regression introduced by the auth-service deploy (auth:v2.4.1-rc3 at 2026-02-10T16:30Z) caused auth p99 latency to spike (~8.2s) and upstream 503s in payment-service.
- Incident response: partly correct (alerting, commander assignment, investigation and ro...
- **smolagents**: Calling tools:
[{'id': 'call_io9nXv3g0bP2kL1zQY7F6', 'type': 'function', 'function': {'name': 'query_infrastructure', 'arguments': {'query': "SELECT i.incident_id, i.title, i.severity, i.status, i.affected_service_id, i.opened_at, i.identified_at, i.resolved_at, i.commander, i.root_cause, t.entry_id...
- **CrewAI**: Thought: I should retrieve the incident record for INC-4001 to see metadata, affected service, timestamps, commander, and any recorded root_cause.
Action: query_infrastructure
Action Input: {"query":"SELECT * FROM incidents WHERE incident_id = 'INC-4001';"}

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 51.08 | 40.81 | 9.67 | 120.00 |
| Tokens | 7,814 | 8,234 | 2,729 | 0 |
| Correctness | 2 | 2 | 1 | 0 |
| Completeness | 2 | 2 | 1 | 0 |
| Faithfulness | 5 | 5 | 1 | 0 |
| Retrieval Prec | 1.00 | 0.33 | 1.00 | 0.00 |
| Retrieval Recall | 0.14 | 0.14 | 0.14 | 0.00 |
| Actual Agents | 2 | 1 | 1 | 0 |
| Agent Coverage | 0.667 | 0.333 | 0.333 | 0 |
| Coordination Points | 5 | 5 | 5 | 5 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0 | 0 |
| Has Tool Trace | 1 | 1 | 1 | 0 |
| Hop Coverage | 0.600 | 0.400 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 3 | 2 | 0 | 0 |
| Matched Tools | 2 | 1 | 1 | 0 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 5 | 5 | 5 | 5 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 | 0 |
| Tool Coverage | 0.667 | 0.333 | 0.333 | 0 |

**Answers:**

- **Pydantic AI**: Summary (what we know)
- Incident: INC-4002 — "order-service degraded performance in eu-west-1"
- Severity: sev2
- Status: investigating
- Affected service: SVC-004
- Opened at: 2026-02-10T14:30:00Z
- Commander: dave@nimbusops.io
- identified_at / root_cause: not recorded yet

I could only retrieve ...
- **LangGraph**: Summary
- Incident: INC-4002 — "order-service degraded performance in eu-west-1" (sev2, investigating). Affected service SVC-004 (order-service), team owner: Commerce. Opened 2026-02-10T14:30Z; commander: dave@nimbusops.io.
- What I could confirm from infra DB: order-service runs in cluster CL-002 (...
- **smolagents**: Calling function: query_infrastructure with service metadata query.
{"id":"call_1","type":"function","function":{"name":"query_infrastructure","arguments":{"query":"SELECT * FROM services WHERE service_id = 'SVC-004';"}}}
- **CrewAI**: Query timed out before producing an answer.

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 32.56 | 30.71 | 7.01 | 93.35 |
| Tokens | 8,139 | 6,207 | 2,483 | 123,326 |
| Correctness | 2 | 3 | 1 | 2 |
| Completeness | 2 | 2 | 1 | 2 |
| Faithfulness | 5 | 5 | 1 | 5 |
| Retrieval Prec | 0.75 | 0.80 | 0.00 | 0.67 |
| Retrieval Recall | 0.43 | 0.57 | 0.00 | 0.29 |
| Actual Agents | 2 | 2 | 1 | 2 |
| Agent Coverage | 0.667 | 0.667 | 0.333 | 0.667 |
| Coordination Points | 4 | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.250 | 0.250 | 0 | 0.250 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 0.500 | 0.500 | 0 | 0.250 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 0 | 1 |
| Matched Tools | 2 | 2 | 1 | 2 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 0.667 | 0.667 | 0.333 | 0.667 |

**Answers:**

- **Pydantic AI**: Summary (what I can confirm)
- Incident: INC-4002 — "order-service degraded performance in eu-west-1"
- Severity: sev2
- Status: investigating
- Incident commander: dave@nimbusops.io
- Source runbook guidance: emergency change process requires the incident commander to explicitly authorize emergency...
- **LangGraph**: Summary (grounded evidence)
- INC-4002: "order-service degraded performance in eu-west-1" — severity = sev2, status = investigating, incident commander = dave@nimbusops.io, affected service = order-service (team_owner: Commerce, tier: critical). (from incidents + services)
- Relevant runbook policy ...
- **smolagents**: I'll query the incidents and incident_timeline tables for INC-4002 to gather the incident details and timeline entries.
Calling tool to fetch incident and timeline details for INC-4002 (1/1)...
- **CrewAI**: Below is a grounded, evidence-backed, complete remediation sequence for INC-4002 (order-service degraded performance in eu-west-1), the required approvals, and the remaining missing evidence you must fetch to finalize approvers and exact SLAs.

Incident summary (evidence)
- Incident: INC-4002 — "ord...

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 36.13 | 48.11 | 10.88 | 79.74 |
| Tokens | 6,804 | 9,771 | 2,744 | 139,881 |
| Correctness | 4 | 2 | 1 | 5 |
| Completeness | 3 | 2 | 1 | 4 |
| Faithfulness | 5 | 5 | 1 | 5 |
| Retrieval Prec | 0.75 | 1.00 | 0.00 | 0.80 |
| Retrieval Recall | 0.50 | 0.33 | 0.00 | 0.67 |
| Actual Agents | 2 | 2 | 1 | 2 |
| Agent Coverage | 0.667 | 0.667 | 0.333 | 0.667 |
| Coordination Points | 3 | 3 | 3 | 3 |
| Coordination Success | 0 | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.500 | 0.250 | 0 | 0.500 |
| Has Tool Trace | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Coordination | 1 | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 | 0 |
| Matched Hops | 4 | 4 | 0 | 4 |
| Matched Tools | 2 | 2 | 1 | 2 |
| Required Agents | 3 | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 | 3 |
| Tool Calls Reported | 3 | 3 | 1 | 3 |
| Tool Coverage | 0.667 | 0.667 | 0.333 | 0.667 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — escalate INC-4002 from sev2 to sev1.

Evidence from data
- Incident record (INC-4002)
  - Title: "order-service degraded performance in eu-west-1"
  - Current severity: sev2, Status: investigating
  - Opened_at: 2026-02-10T14:30:00Z
  - identified_at: NULL (no identification reco...
- **LangGraph**: Short answer: I cannot conclusively decide with the current information because I couldn't retrieve the incident and security evidence from the databases within the tool budget. Escalate INC-4002 from sev2 → sev1 only if one or more of the runbook escalation triggers are met; below I list those trig...
- **smolagents**: Calling tool to fetch the incident record (safe SELECT).
- **CrewAI**: Recommendation: Escalate INC-4002 from sev2 to sev1 immediately.

Evidence from the incident data (incident_timeline / incidents):
- Alert (monitoring-bot) at 2026-02-10T14:30:00Z: "Alert: order-service p95 latency increased to 4500ms in eu-west-1 (baseline: 200ms)." — severe customer-impacting degr...
