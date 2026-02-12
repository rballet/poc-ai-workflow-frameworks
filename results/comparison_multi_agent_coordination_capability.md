# Framework Comparison Report

Generated: 2026-02-12 12:12 UTC
Scenario: multi_agent_coordination
Scenario Type: multi_agent_coordination
Mode: capability
Profile: multi_agent_coordination
Questions: 10

## Summary

| Metric | Pydantic AI |
| --- | --- |
| Avg Latency (s) | 104.24 |
| Total Tokens | 416,866 |
| Est. Cost (USD) | $0.3210 |
| Avg Correctness (1-5) | 4.6 |
| Avg Completeness (1-5) | 4.3 |
| Avg Faithfulness (1-5) | 4.6 |
| Avg Retrieval Precision | 0.42 |
| Avg Retrieval Recall | 0.97 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI |
| --- | --- |
| Capability | 90.0 |
| Efficiency | 33.3 |
| Developer Experience | N/A |

## Runtime Distribution

| Metric | Pydantic AI |
| --- | --- |
| Latency p50 (s) | 91.03 |
| Latency p95 (s) | 181.80 |

## Scenario-Specific Metrics

| Metric | Pydantic AI |
| --- | --- |
| Actual Agents Avg | 2.200 |
| Agent Coverage Avg | 0.967 |
| Coordination Avg Agent Coverage | 0.952 |
| Coordination Avg Grounded Hop Coverage | 0.810 |
| Coordination Avg Hop Coverage | 0.810 |
| Coordination Avg Tool Coverage | 0.952 |
| Coordination Points Avg | 2.200 |
| Coordination Questions | 7 |
| Coordination Success Avg | 0.300 |
| Coordination Success Rate | 0.429 |
| Easy Avg Hop Coverage | 1 |
| Easy Questions | 3 |
| Grounded Hop Coverage Avg | 0.867 |
| Has Tool Trace Avg | 1 |
| Hop Coverage Avg | 0.867 |
| Is Coordination Avg | 0.700 |
| Is Easy Avg | 0.300 |
| Matched Hops Avg | 2.400 |
| Matched Tools Avg | 2 |
| Required Agents Avg | 2.100 |
| Required Hops Avg | 2.800 |
| Required Tools Count Avg | 2.100 |
| Tool Calls Reported Avg | 14.800 |
| Tool Coverage Avg | 0.967 |
| Tool Trace Rate | 1 |

## Per-Question Results

### q1: What services run on the prod-us-east-1 cluster and what are their tiers?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 11.93 |
| Tokens | 2,327 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 1.00 |
| Actual Agents | 1 |
| Agent Coverage | 1 |
| Coordination Points | 0 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Agents | 1 |
| Required Hops | 1 |
| Required Tools Count | 1 |
| Tool Calls Reported | 1 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Services running on cluster prod-us-east-1 and their tiers (from the infrastructure inventory):

- api-gateway — critical  
- auth-service — critical  
- payment-service — critical  
- user-profile — standard

If you want, I can also pull recent deploys, health status, or dependency maps for these s...

### q2: Are there any open critical vulnerabilities? List them with their remediation deadlines.

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 83.51 |
| Tokens | 14,656 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 0.17 |
| Retrieval Recall | 1.00 |
| Actual Agents | 2 |
| Agent Coverage | 1 |
| Coordination Points | 0 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Agents | 1 |
| Required Hops | 1 |
| Required Tools Count | 1 |
| Tool Calls Reported | 7 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — there is 1 open critical vulnerability. Its remediation deadline has passed.

Details (from security + infra records)
- vulnerability_id: SCAN-201
- cve_id / title: CVE-2025-31337 — Remote code execution in container base image
- severity / status: critical / open
- affected serv...

### q3: What are the escalation triggers for promoting a sev2 incident to sev1?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 93.14 |
| Tokens | 48,009 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 4 |
| Retrieval Prec | 0.33 |
| Retrieval Recall | 1.00 |
| Actual Agents | 1 |
| Agent Coverage | 1 |
| Coordination Points | 0 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 0 |
| Is Easy | 1 |
| Matched Hops | 1 |
| Matched Tools | 1 |
| Required Agents | 1 |
| Required Hops | 1 |
| Required Tools Count | 1 |
| Tool Calls Reported | 12 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Summary — when to promote Sev2 → Sev1
Per the incident response runbook, a Sev2 MUST be promoted to Sev1 immediately if any one of the following escalation triggers is met:

1. Cascading impact detected
   - The affected service has downstream dependents that are also degraded or failing.

2. Invest...

### q4: Was the most recent deploy of auth-service compliant with the change management policy?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 194.65 |
| Tokens | 102,333 |
| Correctness | 4 |
| Completeness | 4 |
| Faithfulness | 5 |
| Retrieval Prec | 0.25 |
| Retrieval Recall | 1.00 |
| Actual Agents | 2 |
| Agent Coverage | 1 |
| Coordination Points | 2 |
| Coordination Success | 1 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 3 |
| Matched Tools | 2 |
| Required Agents | 2 |
| Required Hops | 3 |
| Required Tools Count | 2 |
| Tool Calls Reported | 24 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer: No — the most recent production deploy of auth-service (DEP-102 / auth:v2.4.1-rc3 on 2026-02-10T16:30Z) was not compliant with the Change Management Policy.

Evidence summary (grounded in infra + runbook data)
- Deploy record (recent_deploys): DEP-102
  - deployed_at: 2026-02-10T16:30:...

### q5: Was the firewall rule change FW-404 on prod-eu-west-1 properly authorized?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 102.43 |
| Tokens | 59,287 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 0.20 |
| Retrieval Recall | 1.00 |
| Actual Agents | 3 |
| Agent Coverage | 1 |
| Coordination Points | 2 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 0.500 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.500 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 1 |
| Matched Tools | 2 |
| Required Agents | 2 |
| Required Hops | 2 |
| Required Tools Count | 2 |
| Tool Calls Reported | 26 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer: No — based on the available records, the FW-404 change on prod-eu-west-1 was not properly authorized.

Why (evidence):
- Change record: firewall_rules shows FW-404 changed 2026-02-10T12:00:00Z on cluster CL-002 (prod-eu-west-1) to allow ingress tcp:8083 from 198.51.100.0/24. modified_b...

### q6: Which services have both open critical or high vulnerabilities and recent deploys without change tickets?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 60.40 |
| Tokens | 13,290 |
| Correctness | 3 |
| Completeness | 2 |
| Faithfulness | 4 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 1.00 |
| Actual Agents | 2 |
| Agent Coverage | 1 |
| Coordination Points | 2 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 0.667 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.667 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 2 |
| Matched Tools | 2 |
| Required Agents | 2 |
| Required Hops | 3 |
| Required Tools Count | 2 |
| Tool Calls Reported | 6 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer
- No services meet both conditions. There are currently no open CRITICAL or HIGH vulnerabilities in our vulnerability_scans table, and the only recent deploy (last 30 days) without a change ticket is auth-service — but it has no matching open CRITICAL/HIGH findings.

What I checked (evi...

### q7: What is the likely root cause of INC-4001, and was proper incident response followed?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 166.10 |
| Tokens | 40,107 |
| Correctness | 5 |
| Completeness | 4 |
| Faithfulness | 5 |
| Retrieval Prec | 0.67 |
| Retrieval Recall | 1.00 |
| Actual Agents | 2 |
| Agent Coverage | 0.667 |
| Coordination Points | 4 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 0.750 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.750 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 3 |
| Matched Tools | 2 |
| Required Agents | 3 |
| Required Hops | 4 |
| Required Tools Count | 3 |
| Tool Calls Reported | 17 |
| Tool Coverage | 0.667 |

**Answers:**

- **Pydantic AI**: Short answer
- Likely root cause: an auth-service deploy (auth:v2.4.1-rc3, DEP-102) at 2026-02-10T16:30 introduced a latency regression (auth p99 ≈ 8200ms). payment-service synchronously depends on auth, timed out and returned 503s, triggering INC-4001.
- Was incident response proper? Partially — so...

### q8: Provide a full incident analysis for INC-4002: root cause, security posture assessment, and compliance violations.

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 156.86 |
| Tokens | 59,272 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 0.58 |
| Retrieval Recall | 1.00 |
| Actual Agents | 3 |
| Agent Coverage | 1 |
| Coordination Points | 5 |
| Coordination Success | 1 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 5 |
| Matched Tools | 3 |
| Required Agents | 3 |
| Required Hops | 5 |
| Required Tools Count | 3 |
| Tool Calls Reported | 22 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Summary (top-line)
- Probable root cause: A firewall rule (FW-404) was opened to 198.51.100.0/24 at 2026-02-10T12:00:00Z, allowing high-volume anomalous requests (198.51.100.42/.43) to SVC-004 (order-service) on port 8083. That traffic preceded and very likely caused the service degradation (p95 lat...

### q9: If we need to remediate INC-4002, what is the sequence of actions and who needs to approve?

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 88.91 |
| Tokens | 38,564 |
| Correctness | 4 |
| Completeness | 4 |
| Faithfulness | 4 |
| Retrieval Prec | 0.45 |
| Retrieval Recall | 0.71 |
| Actual Agents | 3 |
| Agent Coverage | 1 |
| Coordination Points | 4 |
| Coordination Success | 0 |
| Grounded Hop Coverage | 0.750 |
| Has Tool Trace | 1 |
| Hop Coverage | 0.750 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 3 |
| Matched Tools | 3 |
| Required Agents | 3 |
| Required Hops | 4 |
| Required Tools Count | 3 |
| Tool Calls Reported | 15 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer (plain): follow the Incident Response -> Emergency Change workflow. For INC-4002 (order-service, critical tier, sev2) the immediate remediation sequence is:

1) Triage & declare authority
   - Action: Incident Commander (IC) confirms incident severity and declares containment/repair pla...

### q10: Should INC-4002 be escalated from sev2 to sev1? Justify with evidence from the data and policies.

| Metric | Pydantic AI |
| --- | --- |
| Latency (s) | 84.48 |
| Tokens | 39,021 |
| Correctness | 5 |
| Completeness | 4 |
| Faithfulness | 4 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 1.00 |
| Actual Agents | 3 |
| Agent Coverage | 1 |
| Coordination Points | 3 |
| Coordination Success | 1 |
| Grounded Hop Coverage | 1 |
| Has Tool Trace | 1 |
| Hop Coverage | 1 |
| Is Coordination | 1 |
| Is Easy | 0 |
| Matched Hops | 4 |
| Matched Tools | 3 |
| Required Agents | 3 |
| Required Hops | 4 |
| Required Tools Count | 3 |
| Tool Calls Reported | 18 |
| Tool Coverage | 1 |

**Answers:**

- **Pydantic AI**: Short answer: Yes — escalate INC-4002 from sev2 to sev1 now.

Why (policy + evidence)
- Policy: The runbook mandates escalation from sev2 → sev1 if ANY of these apply: (1) cascading impact detected, (2) incident remains in "investigating" > 60 minutes without identification, (3) anomalous access sug...
