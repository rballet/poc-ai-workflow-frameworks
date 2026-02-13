# Framework Comparison Report

Generated: 2026-02-12 23:11 UTC
Scenario: multihop_qa
Scenario Type: rag_qa
Mode: capability
Profile: multihop_chain_qa
Questions: 9

## Summary

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Latency (s) | 40.05 | 22.92 | 113.22 | 57.77 |
| Total Tokens | 56,613 | 41,006 | 291,212 | 1,334,465 |
| Est. Cost (USD) | $0.0733 | $0.0440 | $0.2037 | $1.9086 |
| Avg Correctness (1-5) | 3.8 | 4.1 | 3.3 | 3.8 |
| Avg Completeness (1-5) | 3.6 | 3.4 | 3.1 | 3.6 |
| Avg Faithfulness (1-5) | 3.9 | 4.0 | 3.3 | 4.4 |
| Avg Retrieval Precision | 0.73 | 0.93 | 0.47 | 0.83 |
| Avg Retrieval Recall | 0.93 | 0.83 | 0.67 | 0.83 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Capability | 75.6 | 67.9 | 66.3 | 80.7 |
| Efficiency | 30.5 | 33.3 | 17.6 | 8.2 |
| Developer Experience | 55.5 | 63.5 | 87.0 | 64.7 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency p50 (s) | 38.78 | 23.57 | 117.51 | 61.13 |
| Latency p95 (s) | 49.19 | 36.26 | 120.00 | 65.56 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Annotated Hop Questions | 6 | 6 | 6 | 6 |
| Chain Success Avg | 0.667 | 0.500 | 0.667 | 0.833 |
| Grounded Hop Coverage Avg | 0.778 | 0.667 | 0.667 | 0.722 |
| Hop Coverage Avg | 0.833 | 0.778 | 0.667 | 0.889 |
| Is Multi Hop Avg | 0.667 | 0.667 | 0.667 | 0.667 |
| Matched Hops Avg | 2.500 | 2.333 | 2 | 2.667 |
| Multi Hop Avg Grounded Hop Coverage | 0.778 | 0.667 | 0.667 | 0.722 |
| Multi Hop Avg Hop Coverage | 0.833 | 0.778 | 0.667 | 0.889 |
| Multi Hop Chain Success Rate | 0.667 | 0.500 | 0.667 | 0.833 |
| Multi Hop Questions | 6 | 6 | 6 | 6 |
| Required Hops Avg | 3 | 3 | 3 | 3 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Source Lines (SLOC) | 284 | 333 | 278 | 324 |
| Comment Ratio | 0% | 0% | 0% | 3% |
| Avg Cyclomatic Complexity | 3.6 | 3.5 | 3.2 | 4.3 |
| Max Cyclomatic Complexity | 11 | 7 | 7 | 17 |
| Complexity Grade | A | A | A | A |
| Maintainability Index | 21.0 | 22.5 | 25.8 | 28.8 |
| Maintainability Grade | A | A | A | A |
| Halstead Volume | 1020 | 842 | 449 | 1356 |
| Halstead Difficulty | 9.0 | 6.7 | 5.9 | 11.6 |
| Halstead Bugs (est.) | 0.34 | 0.28 | 0.15 | 0.45 |
| Total Imports | 10 | 16 | 13 | 10 |
| Framework Imports | 1 | 4 | 2 | 0 |
| Classes | 3 | 2 | 3 | 1 |
| Functions | 13 | 18 | 13 | 16 |
| Type Annotation Coverage | 100% | 94% | 100% | 94% |

## Per-Question Results

### q1: What project runs on server prod-api-03?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 30.51 | 4.85 | 120.00 | 41.55 |
| Tokens | 4,999 | 1,638 | 0 | 15,115 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 5 | 0 | 5 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 0.50 | 1.00 | 0.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The server prod-api-03 runs the "Aurora" project (customer analytics platform). Source: server_registry.md.
- **LangGraph**: The project on prod-api-03 is "Aurora" (customer analytics platform). (Source: server_registry.md)
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: ### prod-api-03
- **Project**: Aurora (customer analytics platform)
- **Rack**: R-415
- **CPU**: 96 vCPU (Intel Xeon w9-3495X)
- **RAM**: 512 GB
- **Storage**: 4 TB NVMe SSD
- **OS**: Ubuntu 24.04 LTS
- **Provisioned**: 2024-06-10
- **Status**: Active

(Source: server_registry.md)

### q2: What are the incident response time guarantees for the Platinum SLA tier?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 38.04 | 8.80 | 117.58 | 47.64 |
| Tokens | 5,401 | 1,716 | 50,390 | 42,932 |
| Correctness | 5 | 4 | 5 | 5 |
| Completeness | 3 | 3 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: Platinum SLA incident response time guarantees: 15 minutes for P1 incidents and 30 minutes for P2 incidents (sla_policies.md).
- **LangGraph**: Platinum SLA: 15 minutes for P1 incidents and 30 minutes for P2 incidents (source: sla_policies.md).
- **smolagents**: Answer (based only on retrieved evidence):

- Incident response time guarantees for the Platinum SLA tier: 15 minutes for P1, 30 minutes for P2.
  - Source: sla_policies.md

Additional context found in the same source:
- Resolution targets (also in sla_policies.md): 1 hour for P1, 4 hours for P2.
- ...
- **CrewAI**: Platinum Tier

- Uptime Guarantee: 99.99% (≤ 4.3 minutes downtime per month)
- Incident Response Time: 15 minutes for P1, 30 minutes for P2
- Resolution Target: 1 hour for P1, 4 hours for P2
- Monitoring: Continuous, 10-second polling intervals
- Failover: Automatic failover with hot standby
- Backu...

### q3: Which datacenter houses the server that runs Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 34.42 | 22.38 | 95.58 | 61.62 |
| Tokens | 6,265 | 4,804 | 46,926 | 74,201 |
| Correctness | 5 | 5 | 5 | 4 |
| Completeness | 4 | 5 | 3 | 3 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 0.67 | 1.00 | 0.50 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Chain Success | 1 | 1 | 1 | 1 |
| Grounded Hop Coverage | 1 | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 | 1 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 3 | 3 | 3 | 3 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The server for Project Aurora (prod-api-03) is in rack R-415 (server_registry.md), which falls within the Portland Datacenter (PDX-1) rack range R-400 through R-499 (datacenter_locations.md).
- **LangGraph**: The Project Aurora server (prod-api-03) is in rack R-415, which falls in the Portland Datacenter (PDX-1) — Meridian Tech, 4520 NW Industrial Way, Portland, OR (Region: us-west). (Sources: server_registry.md; datacenter_locations.md)
- **smolagents**: Answer: The server that runs Project Aurora is housed in the Portland Datacenter (PDX-1).

Supporting evidence (source filenames and excerpts):

- server_registry.md
  - "### prod-api-03
    - **Project**: Aurora (customer analytics platform)
    - **Rack**: R-415"
- datacenter_locations.md
  - "## ...
- **CrewAI**: The server running Project Aurora (prod-api-03) is located in the Portland Datacenter (PDX-1).

Evidence (from provided sources):

From server_registry.md:
### prod-api-03
- **Project**: Aurora (customer analytics platform)
- **Rack**: R-415
- **CPU**: 96 vCPU (Intel Xeon w9-3495X)
- **RAM**: 512 GB...

### q4: Who is the current on-call engineer for the team that owns Project Helios?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 38.78 | 29.71 | 113.10 | 53.76 |
| Tokens | 6,102 | 4,365 | 52,792 | 109,375 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 3 | 5 | 4 |
| Faithfulness | 4 | 4 | 5 | 5 |
| Retrieval Prec | 0.33 | 1.00 | 0.20 | 0.50 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The Payments Engineering team owns Project Helios, and their current on-call primary is Kevin Nakamura (rotation: weekly, current as of 2025-01). (Source: team_directory.md; Helios mapping: server_registry.md)
- **LangGraph**: Kevin Nakamura — On-Call Primary (rotation: weekly, current as of 2025-01). Source: team_directory.md.
- **smolagents**: Answer (evidence-only):

- Owning team: Payments Engineering (Projects Owned: Helios) — source: team_directory.md
- Current on-call engineer (per retrieved evidence): Kevin Nakamura — listed as "On-Call Primary: Kevin Nakamura (rotation: weekly, current as of 2025-01)" in team_directory.md.

Support...
- **CrewAI**: Kevin Nakamura is the current on-call engineer for the team that owns Project Helios.

Evidence (verbatim excerpts from provided context):

[Source: team_directory.md]
## Payments Engineering Team

- **Team Lead**: Rachel Torres
- **Members**: Rachel Torres, Kevin Nakamura, Aisha Mohammed, Ben Stric...

### q5: What was the root cause of the most recent incident that affected the server running Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 41.99 | 17.27 | 120.00 | 66.30 |
| Tokens | 6,936 | 4,435 | 0 | 147,229 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 4 | 0 | 5 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 0.67 | 1.00 | 0.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 0.00 | 1.00 |
| Chain Success | 1 | 1 | 0 | 1 |
| Grounded Hop Coverage | 1 | 1 | 0 | 1 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 3 | 3 | 0 | 3 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The server running Project Aurora is prod-api-03 (server_registry.md). The most recent incident affecting it was INC-2025-042 (2025-01-08); the root cause was a firmware bug in the top-of-rack switch (Arista 7280R3) that caused a spanning tree reconvergence event and a network partition between rack...
- **LangGraph**: prod-api-03 hosts Project Aurora (server_registry.md). The most recent incident affecting that server (INC-2025-042 on 2025-01-08) was caused by a firmware bug in the top-of-rack Arista 7280R3 switch that triggered a spanning-tree reconvergence, producing a network partition between racks R-400 and ...
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: The server running Project Aurora is prod-api-03 (server_registry.md). The most recent incident affecting it is INC-2025-042: Network Partition in Portland Datacenter (incident_log.md).

Root Cause (exact content from incident_log.md):
- **Root Cause**: A firmware bug in the top-of-rack switch (Aris...

### q6: What SLA tier applies to datacenters in the us-west region, and what is its uptime guarantee?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 35.13 | 23.57 | 120.00 | 59.94 |
| Tokens | 4,824 | 4,577 | 0 | 182,954 |
| Correctness | 5 | 5 | 0 | 5 |
| Completeness | 5 | 5 | 0 | 5 |
| Faithfulness | 5 | 5 | 0 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 0.00 | 1.00 |
| Retrieval Recall | 1.00 | 0.50 | 0.00 | 0.50 |
| Chain Success | 1 | 1 | 0 | 1 |
| Grounded Hop Coverage | 1 | 0.667 | 0 | 0.667 |
| Hop Coverage | 1 | 1 | 0 | 1 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 3 | 3 | 0 | 3 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: Gold tier applies to us-west region datacenters. Its uptime guarantee is 99.95% (≤ 21.6 minutes downtime per month). (Source: sla_policies.md)
- **LangGraph**: The us-west datacenters are assigned the Gold tier. Its uptime guarantee is 99.95% (≤ 21.6 minutes downtime per month). (Source: sla_policies.md)
- **smolagents**: Query timed out before producing an answer.
- **CrewAI**: SLA tier that applies to datacenters in the us-west region: Gold Tier.

Uptime Guarantee: 99.95% (≤ 21.6 minutes downtime per month).

Actual content from the provided source showing this:

"The Gold tier covers production workloads that need high availability but can tolerate brief interruptions. M...

### q7: What is the uptime guarantee for the server hosting Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 44.00 | 34.80 | 117.51 | 61.13 |
| Tokens | 6,542 | 5,855 | 46,519 | 218,213 |
| Correctness | 2 | 2 | 5 | 2 |
| Completeness | 2 | 2 | 5 | 2 |
| Faithfulness | 2 | 2 | 5 | 2 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.67 | 0.67 | 1.00 | 1.00 |
| Chain Success | 1 | 0 | 1 | 1 |
| Grounded Hop Coverage | 0.667 | 0.333 | 1 | 1 |
| Hop Coverage | 1 | 0.667 | 1 | 1 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 3 | 2 | 3 | 3 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: I can’t determine the uptime guarantee from the provided documents because there’s no mapping from prod-api-03 (Project Aurora) to a datacenter region or SLA tier.

Evidence:
- prod-api-03 is listed as hosting Project Aurora (server_registry.md).  
- The SLA tiers show Gold = 99.95% uptime (≤ 21.6 m...
- **LangGraph**: prod-api-03 is the server listed as hosting Project Aurora (server_registry.md). However, the provided documents do not state which SLA tier (or datacenter/region) that rack/server is assigned to, so I cannot definitively state its uptime guarantee from the given context (sla_policies.md).

For refe...
- **smolagents**: Uptime guarantee for the server hosting Project Aurora: 99.95% (≤ 21.6 minutes downtime per month).

Supporting evidence (source filenames):
- server_registry.md: shows prod-api-03 is Project: Aurora and is in Rack: R-415.
- datacenter_locations.md: shows Portland Datacenter (PDX-1) is region us-wes...
- **CrewAI**: - The server hosting Project Aurora is prod-api-03 (Project: Aurora, Rack: R-415). (Source: server_registry.md)

- The provided documents do not state which datacenter or region contains rack R-415, so I cannot determine which SLA tier applies to that server and therefore cannot state its uptime gua...

### q8: Which engineer should be contacted about the network partition incident that occurred at the Portland datacenter?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 46.72 | 27.64 | 98.98 | 63.55 |
| Tokens | 6,567 | 5,864 | 43,336 | 252,431 |
| Correctness | 1 | 1 | 5 | 1 |
| Completeness | 1 | 1 | 5 | 1 |
| Faithfulness | 2 | 2 | 5 | 3 |
| Retrieval Prec | 0.67 | 0.67 | 0.75 | 0.50 |
| Retrieval Recall | 0.67 | 0.67 | 1.00 | 0.67 |
| Chain Success | 0 | 0 | 1 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 1 | 0.333 |
| Hop Coverage | 0.333 | 0.333 | 1 | 0.333 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 1 | 1 | 3 | 1 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: Contact Nadia Petrova — Site Reliability Engineering (On‑Call Primary). If she’s unavailable, contact Ryan Walsh (On‑Call Secondary / monitoring & incident response).

Sources: incident_log.md (INC-2025-042), team_directory.md (SRE entry; Ryan Walsh entry).
- **LangGraph**: Contact Ryan Walsh from SRE — he owns monitoring/incident response coordination. (See team_directory.md.)  
The incident is INC-2025-042 (Portland datacenter network partition) in incident_log.md.  
Preferred contact: Slack #sre. Escalation path: Nadia Petrova → Alex Kim → VP Engineering (Dana Kim)....
- **smolagents**: Contact: Priya Patel — Platform Infrastructure on-call primary (current rotation as of 2025-01).
Role: On-call primary for the Platform Infrastructure team (owner of the Aurora project running prod-api-03).
Suggested contact method: Platform Infrastructure Slack channel #team-platform-infra (per tea...
- **CrewAI**: Contact: Ryan Walsh

From team_directory.md:
Ryan Walsh
- **Projects Owned**: Monitoring infrastructure, incident response coordination
- **Slack Channel**: #sre
- **Escalation Path**: Nadia Petrova → Alex Kim → VP Engineering (Dana Kim)

The SRE team does not own application projects directly but p...

### q9: What is the maximum incident response time for P1 incidents affecting Project Helios, given its server's datacenter location?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 50.84 | 37.23 | 116.25 | 64.45 |
| Tokens | 8,977 | 7,752 | 51,249 | 292,015 |
| Correctness | 1 | 5 | 5 | 2 |
| Completeness | 2 | 3 | 5 | 2 |
| Faithfulness | 2 | 3 | 5 | 5 |
| Retrieval Prec | 0.75 | 0.67 | 0.75 | 0.50 |
| Retrieval Recall | 1.00 | 0.67 | 1.00 | 0.33 |
| Chain Success | 0 | 0 | 1 | 1 |
| Grounded Hop Coverage | 0.667 | 0.667 | 1 | 0.333 |
| Hop Coverage | 0.667 | 0.667 | 1 | 1 |
| Is Multi Hop | 1 | 1 | 1 | 1 |
| Matched Hops | 2 | 2 | 3 | 3 |
| Required Hops | 3 | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: I can’t determine a single “maximum” P1 response time from the provided documents because a required mapping is missing.

What the evidence shows
- prod-api-01 is Project Helios and is located in rack R-201 (server_registry.md).  
  (Source: server_registry.md)
- The SLA P1 response for the Platinum...
- **LangGraph**: The maximum P1 incident response time is 15 minutes.

Reasoning: prod-api-01 is the Helios (payment processing) server (server_registry.md), and Platinum SLAs — which are reserved for payment-processing workloads and apply to the us‑east datacenters — specify a 15‑minute P1 response time (sla_polici...
- **smolagents**: Answer: 15 minutes.

Why: 
- prod-api-01 is assigned to Project Helios and is in Rack R-201 (server_registry.md).  
- Rack R-201 is located in the Ashburn datacenter (IAD-1), region us-east (datacenter_locations.md).  
- The SLA document assigns the us-east datacenters to the Platinum tier, which sp...
- **CrewAI**: I cannot determine the maximum P1 incident response time for Project Helios because the datacenter (region) for the affected server (prod-api-01) is not specified in the provided incident record. The incident log (INC-2025-038) lists the affected server but does not state its datacenter or region [S...
