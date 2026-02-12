# Framework Comparison Report

Generated: 2026-02-12 14:54 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: capability
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 95.60 | 137.34 | 241.60 |
| Total Tokens | 331,585 | 310,753 | 0 |
| Est. Cost (USD) | $0.2958 | $0.1831 | $0.0000 |
| Avg Correctness (1-5) | 4.5 | 3.4 | 0.4 |
| Avg Completeness (1-5) | 4.1 | 3.2 | 0.4 |
| Avg Faithfulness (1-5) | 4.7 | 3.5 | 0.4 |
| Avg Retrieval Precision | 0.38 | 0.44 | 0.08 |
| Avg Retrieval Recall | 0.99 | 0.68 | 0.25 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Capability | 88.7 | 67.3 | 8.0 |
| Efficiency | 13.3 | 15.0 | 20.0 |
| Developer Experience | N/A | N/A | N/A |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency p50 (s) | 80.10 | 111.67 | 300.00 |
| Latency p95 (s) | 169.82 | 300.00 | 300.00 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Actual Agents Avg | 2.400 | 1.300 | 0.500 |
| Agent Coverage Avg | 1 | 0.683 | 0.250 |
| Coordination Avg Agent Coverage | 1 | 0.548 | 0.071 |
| Coordination Avg Grounded Hop Coverage | 0.798 | 0.488 | 0 |
| Coordination Avg Hop Coverage | 0.798 | 0.524 | 0 |
| Coordination Avg Tool Coverage | 1 | 0.548 | 0.071 |
| Coordination Points Avg | 2.200 | 2.200 | 2.200 |
| Coordination Questions | 7 | 7 | 7 |
| Coordination Success Avg | 0.300 | 0.200 | 0 |
| Coordination Success Rate | 0.429 | 0.286 | 0 |
| Easy Avg Hop Coverage | 1 | 1 | 0 |
| Easy Questions | 3 | 3 | 3 |
| Grounded Hop Coverage Avg | 0.858 | 0.642 | 0 |
| Has Tool Trace Avg | 1 | 0.800 | 0.400 |
| Hop Coverage Avg | 0.858 | 0.667 | 0 |
| Is Coordination Avg | 0.700 | 0.700 | 0.700 |
| Is Easy Avg | 0.300 | 0.300 | 0.300 |
| Matched Hops Avg | 2.400 | 1.500 | 0 |
| Matched Tools Avg | 2.100 | 1.200 | 0.300 |
| Required Agents Avg | 2.100 | 2.100 | 2.100 |
| Required Hops Avg | 2.800 | 2.800 | 2.800 |
| Required Tools Count Avg | 2.100 | 2.100 | 2.100 |
| Tool Calls Reported Avg | 15.900 | 5.900 | 4.600 |
| Tool Coverage Avg | 1 | 0.683 | 0.250 |
| Tool Trace Rate | 1 | 0.800 | 0.400 |

## Per-Question Results

### q1: What services run on the prod-us-east-1 cluster and what are their tiers?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 16.40 | 23.45 | 145.29 |
| Tokens | 2,547 | 3,427 | 0 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.50 | 0.50 | 0.10 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Actual Agents | 1 | 1 | 2 |
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
| Tool Calls Reported | 1 | 1 | 18 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: I queried the infrastructure inventory for cluster prod-us-east-1. Services and their tiers:

- api-gateway — critical  
- auth-service — critical  
- payment-service — critical  
- user-profile — standard

Source: infrastructure inventory for cluster prod-us-east-1. If you also want service types (...
- **LangGraph**: Summary
- Services running on cluster prod-us-east-1 and their tiers:
  - api-gateway — critical
  - auth-service — critical
  - payment-service — critical
  - user-profile — standard

Evidence (query output)
- Query run: SELECT s.name AS service_name, s.tier FROM services s JOIN clusters c ON s.clu...
- **smolagents**: Agent timed out or was interrupted before producing an answer.

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 74.64 | 78.23 | 164.50 |
| Tokens | 13,418 | 15,754 | 0 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 4 | 1 |
| Retrieval Prec | 0.17 | 1.00 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Actual Agents | 2 | 1 | 1 |
| Agent Coverage | 1 | 1 | 0 |
| Coordination Points | 0 | 0 | 0 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 1 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 0 |
| Is Coordination | 0 | 0 | 0 |
| Is Easy | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 1 | 1 | 0 |
| Required Agents | 1 | 1 | 1 |
| Required Hops | 1 | 1 | 1 |
| Required Tools Count | 1 | 1 | 1 |
| Tool Calls Reported | 5 | 1 | 10 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — there is 1 open critical vulnerability. Details and remediation deadline below.

Vulnerability (open, critical)
- Vulnerability / scan id: SCAN-201  
- CVE: CVE-2025-31337  
- Affected asset: SVC-004 — order-service (running in cluster prod-eu-west-1 / CL-002)  
- Description: Re...
- **LangGraph**: Short answer: Yes — 1 open critical vulnerability. It is overdue.

Evidence (from vulnerability scan)
- scan_id: SCAN-201  
- service_id: SVC-004  
- scanned_at: 2026-02-08T06:00:00Z (UTC)  
- cve_id: CVE-2025-31337  
- description: Remote code execution in container base image  
- status: open  
- ...
- **smolagents**: Agent timed out or was interrupted before producing an answer.

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 47.95 | 66.73 | 128.52 |
| Tokens | 11,756 | 26,558 | 0 |
| Correctness | 5 | 5 | 1 |
| Completeness | 5 | 5 | 1 |
| Faithfulness | 5 | 5 | 1 |
| Retrieval Prec | 0.33 | 0.50 | 0.25 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
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
| Tool Calls Reported | 9 | 4 | 6 |
| Tool Coverage | 1 | 1 | 1 |

**Answers:**

- **Pydantic AI**: Summary — explicit Sev2 → Sev1 escalation triggers (from runbooks)

The runbook defines four MUST-escalate conditions and several concrete thresholds/conditions that require promotion from Sev2 to Sev1. Below are the triggers, grouped with the exact thresholds and the originating policy reference.

...
- **LangGraph**: Below is a concise, evidence‑grounded summary of when a Sev2 must be promoted to Sev1 and what you must do immediately after escalation. All items reference the Incident Response Runbook (incident_response_runbook.md); one procedural note references the Change Management Policy (change_management_po...
- **smolagents**: Agent timed out or was interrupted before producing an answer.

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 161.89 | 76.23 | 177.71 |
| Tokens | 53,349 | 20,849 | 0 |
| Correctness | 3 | 2 | 1 |
| Completeness | 3 | 2 | 1 |
| Faithfulness | 5 | 2 | 1 |
| Retrieval Prec | 0.18 | 0.40 | 0.50 |
| Retrieval Recall | 1.00 | 1.00 | 0.50 |
| Actual Agents | 3 | 2 | 1 |
| Agent Coverage | 1 | 1 | 0.500 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0.667 | 0 |
| Has Tool Trace | 1 | 1 | 1 |
| Hop Coverage | 0.667 | 0.667 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 2 | 0 |
| Matched Tools | 2 | 2 | 1 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 29 | 6 | 12 |
| Tool Coverage | 1 | 1 | 0.500 |

**Answers:**

- **Pydantic AI**: Short answer: No — the most recent deploy (DEP-102) of auth-service was not demonstrably compliant with the change management policy.

Evidence and reasoning
- What we found in the infra DB (grounded facts)
  - recent_deploys: deploy_id = DEP-102, service_name = auth-service, image_tag = auth:v2.4.1...
- **LangGraph**: Synthesis and final determination

Conclusion — Non‑compliant.
- The most recent auth-service deploy (DEP-102) did not meet the change-management policy requirement that “All production deployments MUST have an associated change ticket (CHG-xxxx).” DEP-102 has change_ticket = NULL in the deploy reco...
- **smolagents**: Agent timed out or was interrupted before producing an answer.

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 78.61 | 145.10 | 300.00 |
| Tokens | 32,982 | 67,681 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 5 | 5 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 0.18 | 0.14 | 0.00 |
| Retrieval Recall | 1.00 | 0.50 | 0.00 |
| Actual Agents | 3 | 2 | 0 |
| Agent Coverage | 1 | 0.500 | 0 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.500 | 0.500 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.500 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 1 | 1 | 0 |
| Matched Tools | 2 | 1 | 0 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 2 | 2 | 2 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 26 | 15 | 0 |
| Tool Coverage | 1 | 0.500 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: No — FW-404 was not properly authorized.

Why (evidence)
- FW-404 details (firewall_rules): rule_id = FW-404, cluster_id = CL-002 (prod-eu-west-1), direction = ingress, source_cidr = 198.51.100.0/24, dest_port = 8083, action = allow, last_modified_at = 2026-02-10T12:00:00Z, modified_by...
- **LangGraph**: Conclusion
- No — the firewall change FW-404 on prod-eu-west-1 was not properly authorized.

Evidence (exact data points)
- Firewall record (firewall_rules):
  - rule_id: FW-404
  - cluster_id: CL-002
  - direction: ingress, action: allow
  - source_cidr: 198.51.100.0/24
  - dest_port: 8083 (tcp)
  ...
- **smolagents**: Query timed out before producing an answer.

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 59.29 | 145.75 | 300.00 |
| Tokens | 15,187 | 61,660 | 0 |
| Correctness | 3 | 5 | 0 |
| Completeness | 2 | 4 | 0 |
| Faithfulness | 2 | 5 | 0 |
| Retrieval Prec | 0.40 | 0.33 | 0.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 |
| Actual Agents | 2 | 2 | 0 |
| Agent Coverage | 1 | 1 | 0 |
| Coordination Points | 2 | 2 | 2 |
| Coordination Success | 0 | 1 | 0 |
| Grounded Hop Coverage | 0.667 | 1 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.667 | 1 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 2 | 3 | 0 |
| Matched Tools | 2 | 2 | 0 |
| Required Agents | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |
| Required Tools Count | 2 | 2 | 2 |
| Tool Calls Reported | 7 | 13 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer
- None. I found no services that currently have both (a) an open Critical/High vulnerability and (b) a recent deploy without a change ticket.

Evidence
- Vulnerability query (executed): SELECT service, vulnerability_id, severity, status, scan_date FROM vulnerability_scans WHERE severity...
- **LangGraph**: TL;DR — None. Based on the available datasets, no service meets BOTH conditions (a) has an open critical or high vulnerability and (b) has a recent deploy (last 30 days) that lacks a change ticket.

Grounded evidence (exact data points)
1) Open critical / high vulnerabilities found in vulnerability_...
- **smolagents**: Query timed out before producing an answer.

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 135.27 | 173.15 | 300.00 |
| Tokens | 56,309 | 91,481 | 0 |
| Correctness | 5 | 5 | 0 |
| Completeness | 4 | 4 | 0 |
| Faithfulness | 5 | 5 | 0 |
| Retrieval Prec | 0.50 | 0.50 | 0.00 |
| Retrieval Recall | 1.00 | 0.83 | 0.00 |
| Actual Agents | 3 | 3 | 0 |
| Agent Coverage | 1 | 1 | 0 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 1 | 1 | 0 |
| Grounded Hop Coverage | 1 | 0.750 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 1 | 1 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 4 | 4 | 0 |
| Matched Tools | 3 | 3 | 0 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 23 | 13 | 0 |
| Tool Coverage | 1 | 1 | 0 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: a performance regression introduced by the auth-service deploy (auth:v2.4.1-rc3, DEP-102 at 2026-02-10T16:30:00Z) caused auth-service p99 latency to spike (~8.2s), which caused payment-service outbound calls to auth to time out/fail and generate 503s at the payment-...
- **LangGraph**: Final synthesis — root cause and IR compliance (evidence-grounded)

Likely root cause (concise)
- A performance regression introduced by the auth-service deploy auth:v2.4.1-rc3 at 2026-02-10T16:30:00Z (DEP-102) increased auth p99 latency (~8200 ms vs baseline ~120 ms). That upstream latency caused p...
- **smolagents**: Query timed out before producing an answer.

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 124.06 | 300.00 | 300.00 |
| Tokens | 64,536 | 0 | 0 |
| Correctness | 5 | 0 | 0 |
| Completeness | 5 | 0 | 0 |
| Faithfulness | 5 | 0 | 0 |
| Retrieval Prec | 0.58 | 0.00 | 0.00 |
| Retrieval Recall | 1.00 | 0.00 | 0.00 |
| Actual Agents | 3 | 0 | 0 |
| Agent Coverage | 1 | 0 | 0 |
| Coordination Points | 5 | 5 | 5 |
| Coordination Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0 | 0 |
| Has Tool Trace | 1 | 0 | 0 |
| Hop Coverage | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 5 | 0 | 0 |
| Matched Tools | 3 | 0 | 0 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 5 | 5 | 5 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 25 | 0 | 0 |
| Tool Coverage | 1 | 0 | 0 |

**Answers:**

- **Pydantic AI**: Summary (brief)
- Incident: INC-4002 — "order-service degraded performance in eu-west-1" (SVC-004)
- Opened: 2026-02-10T14:30:00Z; status: investigating; severity: Sev2 (commander: dave@nimbusops.io)
- Quick high-level conclusion (probable root cause): unauthorized/automated firewall change opened o...
- **LangGraph**: Query timed out before producing an answer.
- **smolagents**: Query timed out before producing an answer.

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 81.59 | 64.75 | 300.00 |
| Tokens | 33,949 | 23,343 | 0 |
| Correctness | 4 | 2 | 0 |
| Completeness | 3 | 2 | 0 |
| Faithfulness | 5 | 4 | 0 |
| Retrieval Prec | 0.50 | 1.00 | 0.00 |
| Retrieval Recall | 0.86 | 0.43 | 0.00 |
| Actual Agents | 3 | 1 | 0 |
| Agent Coverage | 1 | 0.333 | 0 |
| Coordination Points | 4 | 4 | 4 |
| Coordination Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.750 | 0.500 | 0 |
| Has Tool Trace | 1 | 1 | 0 |
| Hop Coverage | 0.750 | 0.500 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 3 | 2 | 0 |
| Matched Tools | 3 | 1 | 0 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 17 | 6 | 0 |
| Tool Coverage | 1 | 0.333 | 0 |

**Answers:**

- **Pydantic AI**: Short answer (TL;DR)
- Remediation for INC-4002 (order-service / SVC-004, Sev2 with security indicators) should follow a containment → investigation → patch/rollback → verify → close sequence.
- Key approvers:
  - Incident Commander (dave@nimbusops.io) — must explicitly authorize any emergency/fast-...
- **LangGraph**: Below is a single, actionable remediation sequence for INC-4002 plus the required approvers and the policy citations that justify each step. I’ve split into two paths (Emergency/Sev1 vs Normal) because the required sequence and approvers differ materially.

If you want a ready-to-send retro CHG or a...
- **smolagents**: Query timed out before producing an answer.

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 176.32 | 300.00 | 300.00 |
| Tokens | 47,552 | 0 | 0 |
| Correctness | 5 | 0 | 0 |
| Completeness | 4 | 0 | 0 |
| Faithfulness | 5 | 0 | 0 |
| Retrieval Prec | 0.50 | 0.00 | 0.00 |
| Retrieval Recall | 1.00 | 0.00 | 0.00 |
| Actual Agents | 3 | 0 | 0 |
| Agent Coverage | 1 | 0 | 0 |
| Coordination Points | 3 | 3 | 3 |
| Coordination Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 1 | 0 | 0 |
| Has Tool Trace | 1 | 0 | 0 |
| Hop Coverage | 1 | 0 | 0 |
| Is Coordination | 1 | 1 | 1 |
| Is Easy | 0 | 0 | 0 |
| Matched Hops | 4 | 0 | 0 |
| Matched Tools | 3 | 0 | 0 |
| Required Agents | 3 | 3 | 3 |
| Required Hops | 4 | 4 | 4 |
| Required Tools Count | 3 | 3 | 3 |
| Tool Calls Reported | 17 | 0 | 0 |
| Tool Coverage | 1 | 0 | 0 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — escalate INC-4002 to Sev1 immediately.

Why (evidence → policy → conclusion)

1) Policy: mandatory Sev2→Sev1 triggers
- Runbook: "A Sev2 incident MUST be escalated to Sev1 if ANY of the following are true: Cascading impact detected; Incident remains in 'investigating' status for ...
- **LangGraph**: Query timed out before producing an answer.
- **smolagents**: Query timed out before producing an answer.
