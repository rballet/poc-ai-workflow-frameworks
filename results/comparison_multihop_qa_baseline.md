# Framework Comparison Report

Generated: 2026-02-10 22:50 UTC
Scenario: multihop_qa
Scenario Type: rag_qa
Mode: baseline
Profile: multihop_chain_qa
Questions: 9

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 2.09 | 1.28 | 1.42 |
| Total Tokens | 5,059 | 4,897 | 4,891 |
| Est. Cost (USD) | $0.0010 | $0.0009 | $0.0009 |
| Avg Correctness (1-5) | 3.7 | 3.0 | 3.9 |
| Avg Completeness (1-5) | 3.2 | 2.7 | 3.4 |
| Avg Faithfulness (1-5) | 4.2 | 3.8 | 4.4 |
| Avg Retrieval Precision | 0.89 | 0.89 | 0.89 |
| Avg Retrieval Recall | 0.70 | 0.70 | 0.70 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Annotated Hop Questions | 6 | 6 | 6 |
| Chain Success Avg | 0.167 | 0 | 0 |
| Grounded Hop Coverage Avg | 0.278 | 0.167 | 0.333 |
| Hop Coverage Avg | 0.444 | 0.278 | 0.444 |
| Is Multi Hop Avg | 0.667 | 0.667 | 0.667 |
| Matched Hops Avg | 1.333 | 0.833 | 1.333 |
| Multi Hop Avg Grounded Hop Coverage | 0.278 | 0.167 | 0.333 |
| Multi Hop Avg Hop Coverage | 0.444 | 0.278 | 0.444 |
| Multi Hop Chain Success Rate | 0.167 | 0 | 0 |
| Multi Hop Questions | 6 | 6 | 6 |
| Required Hops Avg | 3 | 3 | 3 |

## Per-Question Results

### q1: What project runs on server prod-api-03?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.07 | 0.91 | 2.27 |
| Tokens | 700 | 697 | 693 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The project that runs on server prod-api-03 is Aurora, which is a customer analytics platform (source: server_registry.md).
- **LangGraph**: The project that runs on server prod-api-03 is Aurora (customer analytics platform) as stated in the server registry document.
- **smolagents**: The project that runs on server prod-api-03 is Aurora, which is a customer analytics platform. [Source: server_registry.md]

### q2: What are the incident response time guarantees for the Platinum SLA tier?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.68 | 0.89 | 0.76 |
| Tokens | 467 | 448 | 434 |
| Correctness | 5 | 5 | 5 |
| Completeness | 3 | 3 | 3 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for Priority 1 (P1) incidents and 30 minutes for Priority 2 (P2) incidents. This information is sourced from the SLA Policies document (sla_policies.md).
- **LangGraph**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents, as stated in the SLA Policies document.
- **smolagents**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents.

### q3: Which datacenter houses the server that runs Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 3.31 | 2.05 | 2.28 |
| Tokens | 623 | 592 | 585 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 2 | 3 | 3 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0.333 | 0.333 |
| Hop Coverage | 0 | 0.333 | 0.333 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 0 | 1 | 1 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The server running Project Aurora is housed in the Ashburn Datacenter (IAD-1). This datacenter is suitable for handling workloads that require proximity to financial networks, which would be relevant for a customer analytics platform like Aurora. The specific evidence regarding the datacenter's capa...
- **LangGraph**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is the primary east coast facility and handles latency-sensitive workloads. The server for Project Aurora is located in rack R-415, which is within the rack range of the Ashburn datacenter (R-200 through R-299) [s...
- **smolagents**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is the primary east coast facility that handles latency-sensitive workloads and is located in the Virginia data center corridor. The server for Project Aurora is located in Rack R-415, which is within the range of...

### q4: Who is the current on-call engineer for the team that owns Project Helios?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.43 | 1.19 | 0.67 |
| Tokens | 490 | 474 | 453 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura. This is based on the team directory that indicates Kevin Nakamura is the On-Call Primary as of January 2025 [team_directory.md].
- **LangGraph**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura (as of 2025-01) [Source: team_directory.md].
- **smolagents**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura.

### q5: What was the root cause of the most recent incident that affected the server running Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.11 | 0.81 | 1.62 |
| Tokens | 576 | 509 | 549 |
| Correctness | 3 | 1 | 5 |
| Completeness | 3 | 1 | 5 |
| Faithfulness | 4 | 1 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.50 |
| Chain Success | 1 | 0 | 0 |
| Grounded Hop Coverage | 0.667 | 0 | 0.667 |
| Hop Coverage | 1 | 0 | 0.667 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 3 | 0 | 2 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The incident that affected the server running Project Aurora is not specified in the provided evidence. The most recent incident listed is INC-2025-042, which affected the "prod-api-03" server. This incident's root cause was a firmware bug in the top-of-rack switch, which caused a network partition....
- **LangGraph**: The provided context does not contain any information about an incident specifically related to a server running Project Aurora. Therefore, I cannot provide the root cause of such an incident.
- **smolagents**: The most recent incident affecting the server running Project Aurora is INC-2025-042, which involved a network partition in the Portland Datacenter. The root cause of this incident was a firmware bug in the top-of-rack switch (Arista 7280R3) that caused a spanning tree reconvergence event, resulting...

### q6: What SLA tier applies to datacenters in the us-west region, and what is its uptime guarantee?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.69 | 2.56 | 1.68 |
| Tokens | 498 | 504 | 495 |
| Correctness | 3 | 3 | 3 |
| Completeness | 3 | 4 | 4 |
| Faithfulness | 4 | 4 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.50 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 0.333 |
| Hop Coverage | 0.667 | 0.667 | 0.667 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The Gold tier applies to datacenters in the us-west region. Its uptime guarantee is 99.9%, allowing for up to 43.2 minutes of downtime per month (Source: sla_policies.md).
- **LangGraph**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) according to the source document "sla_policies.md."
- **smolagents**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) [source: sla_policies.md].

### q7: What is the uptime guarantee for the server hosting Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.75 | 1.24 | 1.09 |
| Tokens | 603 | 606 | 599 |
| Correctness | 5 | 1 | 5 |
| Completeness | 4 | 1 | 3 |
| Faithfulness | 5 | 3 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.67 | 0.67 | 0.67 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0 | 0.333 |
| Hop Coverage | 0.333 | 0 | 0.333 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 1 | 0 | 1 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The uptime guarantee for the server hosting Project Aurora is 99.95% (≤ 21.6 minutes downtime per month), as it falls under the Gold Tier. This information is sourced from the SLA Policies document (sla_policies.md).
- **LangGraph**: The uptime guarantee for the server hosting Project Aurora is not specified in the provided context. The context includes details about the Gold and Silver tiers, but it does not explicitly state which tier applies to Project Aurora. Therefore, I cannot determine the uptime guarantee for that specif...
- **smolagents**: The uptime guarantee for the server hosting Project Aurora is 99.95%, as it falls under the Gold tier of the service level agreement (SLA) policies. This tier is designed for production workloads that require high availability. [Source: sla_policies.md]

### q8: Which engineer should be contacted about the network partition incident that occurred at the Portland datacenter?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.42 | 0.76 | 1.03 |
| Tokens | 569 | 536 | 545 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 3 | 3 | 3 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 0.33 | 0.33 | 0.33 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0 |
| Hop Coverage | 0 | 0 | 0 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 0 | 0 | 0 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The evidence does not specify the name of the engineer to contact regarding the network partition incident at the Portland datacenter. It only mentions the network engineering team applied a firmware patch and that the incident was led by the SRE team for the post-incident review. More specific info...
- **LangGraph**: The provided context does not specify which engineer should be contacted regarding the network partition incident at the Portland datacenter. Key facts about the responsible personnel or contact information are missing.
- **smolagents**: The incident log does not specify a particular engineer to contact regarding the network partition incident. It only mentions that the resolution was handled by the network engineering team. For specific contact information, you may need to refer to internal communication channels or organizational ...

### q9: What is the maximum incident response time for P1 incidents affecting Project Helios, given its server's datacenter location?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.35 | 1.12 | 1.35 |
| Tokens | 533 | 531 | 538 |
| Correctness | 5 | 5 | 5 |
| Completeness | 4 | 3 | 4 |
| Faithfulness | 5 | 5 | 4 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 0.33 | 0.33 | 0.33 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0.333 | 0.333 |
| Hop Coverage | 0.667 | 0.667 | 0.667 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 2 | 2 | 2 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The maximum incident response time for P1 incidents affecting Project Helios, which is located in the us-east region datacenters, is 15 minutes (as specified in the service level agreement policies in sla_policies.md).
- **LangGraph**: The maximum incident response time for P1 incidents affecting Project Helios, which is located in the us-east region datacenters, is 15 minutes, as specified in the SLA policies (source: sla_policies.md).
- **smolagents**: The maximum incident response time for P1 incidents affecting Project Helios, which is located in the us-east region datacenters, is 15 minutes. This is specified in the SLA policies for the Platinum tier, which applies to workloads requiring the highest availability, such as payment processing syst...
