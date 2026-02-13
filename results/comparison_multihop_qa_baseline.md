# Framework Comparison Report

Generated: 2026-02-12 18:59 UTC
Scenario: multihop_qa
Scenario Type: rag_qa
Mode: baseline
Profile: multihop_chain_qa
Questions: 9

## Summary

| Metric | CrewAI |
| --- | --- |
| Avg Latency (s) | 14.45 |
| Total Tokens | 85,314 |
| Est. Cost (USD) | $0.1185 |
| Avg Correctness (1-5) | 3.9 |
| Avg Completeness (1-5) | 3.7 |
| Avg Faithfulness (1-5) | 4.7 |
| Avg Retrieval Precision | 0.89 |
| Avg Retrieval Recall | 0.70 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | CrewAI |
| --- | --- |
| Capability | 64.8 |
| Efficiency | 33.3 |
| Developer Experience | 98.0 |

## Runtime Distribution

| Metric | CrewAI |
| --- | --- |
| Latency p50 (s) | 15.23 |
| Latency p95 (s) | 17.31 |

## Scenario-Specific Metrics

| Metric | CrewAI |
| --- | --- |
| Annotated Hop Questions | 6 |
| Chain Success Avg | 0.500 |
| Grounded Hop Coverage Avg | 0.500 |
| Hop Coverage Avg | 0.778 |
| Is Multi Hop Avg | 0.667 |
| Matched Hops Avg | 2.333 |
| Multi Hop Avg Grounded Hop Coverage | 0.500 |
| Multi Hop Avg Hop Coverage | 0.778 |
| Multi Hop Chain Success Rate | 0.500 |
| Multi Hop Questions | 6 |
| Required Hops Avg | 3 |

## Code Quality — Static Metrics

| Metric | CrewAI |
| --- | --- |
| Source Lines (SLOC) | 324 |
| Comment Ratio | 3% |
| Avg Cyclomatic Complexity | 4.3 |
| Max Cyclomatic Complexity | 17 |
| Complexity Grade | A |
| Maintainability Index | 28.8 |
| Maintainability Grade | A |
| Halstead Volume | 1356 |
| Halstead Difficulty | 11.6 |
| Halstead Bugs (est.) | 0.45 |
| Total Imports | 10 |
| Framework Imports | 0 |
| Classes | 1 |
| Functions | 16 |
| Type Annotation Coverage | 94% |

## Per-Question Results

### q1: What project runs on server prod-api-03?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 9.43 |
| Tokens | 1,553 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 1.00 |
| Is Multi Hop | 0 |

**Answers:**

- **CrewAI**: ### prod-api-03
- **Project**: Aurora (customer analytics platform)
- **Rack**: R-415
- **CPU**: 96 vCPU (Intel Xeon w9-3495X)
- **RAM**: 512 GB
- **Storage**: 4 TB NVMe SSD
- **OS**: Ubuntu 24.04 LTS
- **Provisioned**: 2024-06-10
- **Status**: Active

Answer: The project running on server prod-api-...

### q2: What are the incident response time guarantees for the Platinum SLA tier?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 17.40 |
| Tokens | 3,642 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 4 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 1.00 |
| Is Multi Hop | 0 |

**Answers:**

- **CrewAI**: Platinum Tier

- **Uptime Guarantee**: 99.99% (≤ 4.3 minutes downtime per month)
- **Incident Response Time**: 15 minutes for P1, 30 minutes for P2
- **Resolution Target**: 1 hour for P1, 4 hours for P2
- **Monitoring**: Continuous, 10-second polling intervals
- **Failover**: Automatic failover with...

### q3: Which datacenter houses the server that runs Project Aurora?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 14.15 |
| Tokens | 5,525 |
| Correctness | 3 |
| Completeness | 3 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 1.00 |
| Chain Success | 0 |
| Grounded Hop Coverage | 0.667 |
| Hop Coverage | 0.667 |
| Is Multi Hop | 1 |
| Matched Hops | 2 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: Provided evidence:

From server_registry.md:
### prod-api-03
- **Project**: Aurora (customer analytics platform)
- **Rack**: R-415
- **CPU**: 96 vCPU (Intel Xeon w9-3495X)
- **RAM**: 512 GB
- **Storage**: 4 TB NVMe SSD
- **OS**: Ubuntu 24.04 LTS
- **Provisioned**: 2024-06-10
- **Status**: Active
(So...

### q4: Who is the current on-call engineer for the team that owns Project Helios?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 11.09 |
| Tokens | 7,213 |
| Correctness | 5 |
| Completeness | 5 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 1.00 |
| Is Multi Hop | 0 |

**Answers:**

- **CrewAI**: ## Payments Engineering Team

- **Team Lead**: Rachel Torres
- **Members**: Rachel Torres, Kevin Nakamura, Aisha Mohammed, Ben Strickland
- **On-Call Primary**: Kevin Nakamura (rotation: weekly, current as of 2025-01)
- **On-Call Secondary**: Aisha Mohammed
- **Projects Owned**: Helios (payment proc...

### q5: What was the root cause of the most recent incident that affected the server running Project Aurora?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 15.83 |
| Tokens | 9,348 |
| Correctness | 5 |
| Completeness | 4 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.50 |
| Chain Success | 1 |
| Grounded Hop Coverage | 0.667 |
| Hop Coverage | 1 |
| Is Multi Hop | 1 |
| Matched Hops | 3 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: The provided context does not identify which server runs "Project Aurora", so I cannot determine definitively which incident affected it. What is missing: an explicit mapping from "Project Aurora" to a server name (for example, prod-api-03 or prod-api-01) or an incident entry that names Project Auro...

### q6: What SLA tier applies to datacenters in the us-west region, and what is its uptime guarantee?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 12.95 |
| Tokens | 11,173 |
| Correctness | 3 |
| Completeness | 2 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.50 |
| Chain Success | 0 |
| Grounded Hop Coverage | 0.333 |
| Hop Coverage | 0.667 |
| Is Multi Hop | 1 |
| Matched Hops | 2 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: Based on the provided context from sla_policies.md:

- The SLA tier that applies to datacenters in the us-west region:
  "es To**: us-west region datacenters

  The Gold tier covers production workloads that need high availability but can tolerate brief interruptions. Manual failover procedures are ...

### q7: What is the uptime guarantee for the server hosting Project Aurora?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 15.23 |
| Tokens | 13,340 |
| Correctness | 3 |
| Completeness | 3 |
| Faithfulness | 5 |
| Retrieval Prec | 1.00 |
| Retrieval Recall | 0.67 |
| Chain Success | 1 |
| Grounded Hop Coverage | 0.667 |
| Hop Coverage | 1 |
| Is Multi Hop | 1 |
| Matched Hops | 3 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: Extracts from the provided context:

From server_registry.md:
### prod-api-03
- **Project**: Aurora (customer analytics platform)
- **Rack**: R-415
- **CPU**: 96 vCPU (Intel Xeon w9-3495X)
- **RAM**: 512 GB
- **Storage**: 4 TB NVMe SSD
- **OS**: Ubuntu 24.04 LTS
- **Provisioned**: 2024-06-10
- **Sta...

### q8: Which engineer should be contacted about the network partition incident that occurred at the Portland datacenter?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 17.17 |
| Tokens | 15,730 |
| Correctness | 1 |
| Completeness | 3 |
| Faithfulness | 5 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 0.33 |
| Chain Success | 0 |
| Grounded Hop Coverage | 0.333 |
| Hop Coverage | 0.333 |
| Is Multi Hop | 1 |
| Matched Hops | 1 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: Provided relevant excerpts (verbatim) from the supplied sources:

[Source: incident_log.md]
# Meridian Tech — Incident Log

## INC-2025-042: Network Partition in Portland Datacenter

- **Date**: 2025-01-08 03:22 UTC
- **Severity**: P1
- **Status**: Resolved
- **Affected Server**: prod-api-03
- **Dur...

### q9: What is the maximum incident response time for P1 incidents affecting Project Helios, given its server's datacenter location?

| Metric | CrewAI |
| --- | --- |
| Latency (s) | 16.78 |
| Tokens | 17,790 |
| Correctness | 5 |
| Completeness | 3 |
| Faithfulness | 3 |
| Retrieval Prec | 0.50 |
| Retrieval Recall | 0.33 |
| Chain Success | 1 |
| Grounded Hop Coverage | 0.333 |
| Hop Coverage | 1 |
| Is Multi Hop | 1 |
| Matched Hops | 3 |
| Required Hops | 3 |

**Answers:**

- **CrewAI**: The maximum incident response time for P1 incidents affecting Project Helios is 15 minutes.

Supporting evidence (from provided documents):
- sla_policies.md: "Response Time**: 15 minutes for P1, 30 minutes for P2" (shows P1 response time = 15 minutes). [sla_policies.md]
- sla_policies.md: "Applies ...
