# Framework Comparison Report

Generated: 2026-02-10 20:50 UTC
Scenario: multihop_qa
Questions: 9

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 1.81 | 1.20 | 1.12 |
| Total Tokens | 4,932 | 4,947 | 4,908 |
| Est. Cost (USD) | $0.0009 | $0.0009 | $0.0009 |
| Avg Correctness (1-5) | 3.0 | 3.0 | 3.0 |
| Avg Completeness (1-5) | 2.8 | 2.7 | 2.9 |
| Avg Faithfulness (1-5) | 3.8 | 3.6 | 3.7 |
| Avg Retrieval Precision | 0.89 | 0.89 | 0.89 |
| Avg Retrieval Recall | 0.70 | 0.70 | 0.70 |

## Per-Question Results

### q1: What project runs on server prod-api-03?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.29 | 1.08 | 0.88 |
| Tokens | 702 | 703 | 703 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: The project running on server prod-api-03 is Aurora (customer analytics platform) [Source: server_registry.md].
- **LangGraph**: The project that runs on server prod-api-03 is Aurora (customer analytics platform) [Source: server_registry.md].
- **smolagents**: The project that runs on server prod-api-03 is Aurora (customer analytics platform) [Source: server_registry.md].

### q2: What are the incident response time guarantees for the Platinum SLA tier?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.30 | 1.26 | 1.12 |
| Tokens | 461 | 460 | 460 |
| Correctness | 5 | 5 | 5 |
| Completeness | 3 | 3 | 4 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for a P1 incident and 30 minutes for a P2 incident, as stated in the source document "sla_policies.md".
- **LangGraph**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents. This information is sourced from the document "sla_policies.md."
- **smolagents**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents. This information is sourced from the document "sla_policies.md".

### q3: Which datacenter houses the server that runs Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.63 | 2.70 | 1.26 |
| Tokens | 595 | 627 | 562 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 3 | 3 | 3 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1). This is indicated in the context from the source document "datacenter_locations.md," which describes the Ashburn datacenter as handling workloads that require proximity to financial networks on the east coast. The serve...
- **LangGraph**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is the primary east coast facility mentioned in the context. The server is located in Rack R-415, but the specific datacenter for this rack is not explicitly stated in the server registry. However, since the Ashbu...
- **smolagents**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is the primary east coast facility that handles latency-sensitive workloads. This information is derived from the context provided in the source documents.

### q4: Who is the current on-call engineer for the team that owns Project Helios?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.47 | 1.11 | 1.05 |
| Tokens | 481 | 481 | 481 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura (as of 2025-01) [Source: team_directory.md].
- **LangGraph**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura (as of 2025-01) [Source: team_directory.md].
- **smolagents**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura (as of 2025-01) [Source: team_directory.md].

### q5: What was the root cause of the most recent incident that affected the server running Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.35 | 0.76 | 1.33 |
| Tokens | 509 | 509 | 509 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 1 | 1 | 1 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.50 |

**Answers:**

- **Pydantic AI**: The context does not mention any incidents specifically related to Project Aurora, and thus, there is not enough information to answer the question.
- **LangGraph**: The provided context does not contain any information about an incident affecting a server running Project Aurora. Therefore, I cannot answer the question.
- **smolagents**: The provided context does not contain any information about an incident affecting the server running Project Aurora. Therefore, I cannot answer the question.

### q6: What SLA tier applies to datacenters in the us-west region, and what is its uptime guarantee?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 2.94 | 1.16 | 1.33 |
| Tokens | 512 | 511 | 511 |
| Correctness | 3 | 3 | 3 |
| Completeness | 4 | 4 | 4 |
| Faithfulness | 4 | 4 | 4 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.50 | 0.50 | 0.50 |

**Answers:**

- **Pydantic AI**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) as mentioned in the source document "sla_policies.md."
- **LangGraph**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) according to the source document "sla_policies.md."
- **smolagents**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) according to the source document "sla_policies.md."

### q7: What is the uptime guarantee for the server hosting Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.41 | 0.87 | 0.77 |
| Tokens | 584 | 584 | 584 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 3 | 3 | 3 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 0.67 | 0.67 | 0.67 |

**Answers:**

- **Pydantic AI**: The context does not provide information regarding the uptime guarantee for the server hosting Project Aurora. Therefore, I cannot answer the question.
- **LangGraph**: The context does not provide information about the uptime guarantee for the server hosting Project Aurora. Therefore, I cannot answer the question.
- **smolagents**: The context does not provide information about the uptime guarantee for the server hosting Project Aurora. Therefore, I cannot answer the question.

### q8: Which engineer should be contacted about the network partition incident that occurred at the Portland datacenter?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.50 | 0.70 | 0.82 |
| Tokens | 544 | 531 | 539 |
| Correctness | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 |
| Faithfulness | 3 | 1 | 2 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 0.33 | 0.33 | 0.33 |

**Answers:**

- **Pydantic AI**: The provided context does not specify which engineer should be contacted regarding the network partition incident at the Portland datacenter. Therefore, I cannot answer the question based on the available information.
- **LangGraph**: The provided context does not specify which engineer should be contacted regarding the network partition incident at the Portland datacenter.
- **smolagents**: The provided context does not specify which engineer should be contacted regarding the network partition incident at the Portland datacenter. Therefore, I cannot provide an answer.

### q9: What is the maximum incident response time for P1 incidents affecting Project Helios, given its server's datacenter location?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 1.38 | 1.14 | 1.54 |
| Tokens | 544 | 541 | 559 |
| Correctness | 5 | 5 | 5 |
| Completeness | 4 | 3 | 4 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.50 | 0.50 | 0.50 |
| Retrieval Recall | 0.33 | 0.33 | 0.33 |

**Answers:**

- **Pydantic AI**: The maximum incident response time for P1 incidents affecting Project Helios, which operates in the us-east region datacenters, is 15 minutes. This is based on the SLA policies outlined in the provided context from the document "sla_policies.md".
- **LangGraph**: The maximum incident response time for P1 incidents affecting Project Helios, which is in the us-east region datacenters, is 15 minutes. This is based on the SLA policies outlined in the source document "sla_policies.md."
- **smolagents**: The maximum incident response time for P1 incidents affecting Project Helios, which is associated with the us-east region datacenters, is 15 minutes. This is specified in the SLA policies for the Platinum tier, which applies to workloads requiring the highest availability, such as payment processing...
