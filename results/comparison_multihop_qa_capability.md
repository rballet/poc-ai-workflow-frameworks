# Framework Comparison Report

Generated: 2026-02-10 22:49 UTC
Scenario: multihop_qa
Scenario Type: rag_qa
Mode: capability
Profile: multihop_chain_qa
Questions: 9

## Summary

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Avg Latency (s) | 7.46 | 6.58 | 33.39 |
| Total Tokens | 15,787 | 26,491 | 210,129 |
| Est. Cost (USD) | $0.0034 | $0.0049 | $0.0375 |
| Avg Correctness (1-5) | 4.2 | 3.6 | 5.0 |
| Avg Completeness (1-5) | 3.7 | 3.4 | 4.4 |
| Avg Faithfulness (1-5) | 4.8 | 4.2 | 4.9 |
| Avg Retrieval Precision | 0.81 | 0.84 | 0.82 |
| Avg Retrieval Recall | 0.93 | 0.91 | 0.87 |

## Scenario-Specific Metrics

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Annotated Hop Questions | 6 | 6 | 6 |
| Chain Success Avg | 0.333 | 0.333 | 0.667 |
| Grounded Hop Coverage Avg | 0.500 | 0.444 | 0.833 |
| Hop Coverage Avg | 0.500 | 0.500 | 0.889 |
| Is Multi Hop Avg | 0.667 | 0.667 | 0.667 |
| Matched Hops Avg | 1.500 | 1.500 | 2.667 |
| Multi Hop Avg Grounded Hop Coverage | 0.500 | 0.444 | 0.833 |
| Multi Hop Avg Hop Coverage | 0.500 | 0.500 | 0.889 |
| Multi Hop Chain Success Rate | 0.333 | 0.333 | 0.667 |
| Multi Hop Questions | 6 | 6 | 6 |
| Required Hops Avg | 3 | 3 | 3 |

## Per-Question Results

### q1: What project runs on server prod-api-03?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 5.29 | 9.90 | 46.33 |
| Tokens | 1,055 | 3,344 | 29,800 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 4 |
| Faithfulness | 5 | 5 | 4 |
| Retrieval Prec | 1.00 | 0.50 | 0.33 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The project that runs on server prod-api-03 is Aurora, which is a customer analytics platform [source: server_registry.md].
- **LangGraph**: The project that runs on server prod-api-03 is Aurora, which is a customer analytics platform (source: server_registry.md).
- **smolagents**: Based on the information retrieved, here is the final answer to the question regarding the project running on server `prod-api-03`:

### Final Answer:
The project running on server **prod-api-03** is **Aurora**, which is a customer analytics platform. 

- **Server Details**:
  - **Rack**: R-415
  - ...

### q2: What are the incident response time guarantees for the Platinum SLA tier?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 4.75 | 2.09 | 15.03 |
| Tokens | 961 | 928 | 8,296 |
| Correctness | 5 | 5 | 5 |
| Completeness | 3 | 3 | 3 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for Priority 1 (P1) incidents and 30 minutes for Priority 2 (P2) incidents [source: sla_policies.md].
- **LangGraph**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents, as stated in the SLA Policies document.
- **smolagents**: The incident response time guarantees for the Platinum SLA tier are 15 minutes for P1 incidents and 30 minutes for P2 incidents. Source: sla_policies.md

### q3: Which datacenter houses the server that runs Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 12.25 | 6.88 | 41.55 |
| Tokens | 2,507 | 3,239 | 28,988 |
| Correctness | 1 | 1 | 5 |
| Completeness | 1 | 1 | 5 |
| Faithfulness | 5 | 3 | 5 |
| Retrieval Prec | 0.67 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Chain Success | 0 | 0 | 1 |
| Grounded Hop Coverage | 0 | 0.333 | 1 |
| Hop Coverage | 0 | 0.333 | 1 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 0 | 1 | 3 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is listed under the server registry with details related to the projects owned by the Platform Infrastructure Team, which includes Aurora. The Ashburn Datacenter is specified as the primary east coast facility, wh...
- **LangGraph**: The server that runs Project Aurora is housed in the Ashburn Datacenter (IAD-1), as it is located in rack R-415, which falls within the rack range of the Ashburn facility. This information is derived from the server registry and the details of the Ashburn datacenter provided in the context.
- **smolagents**: Based on the information retrieved through iterative queries, here is the final answer to the question:

**Final Answer:**
The server that runs Project Aurora, identified as **prod-api-03**, is housed in the **Portland Datacenter (PDX-1)**, which accommodates Rack **R-415**.

**Source Filenames:**
-...

### q4: Who is the current on-call engineer for the team that owns Project Helios?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 4.67 | 2.13 | 13.43 |
| Tokens | 1,286 | 976 | 8,313 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 3 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.50 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Is Multi Hop | 0 | 0 | 0 |

**Answers:**

- **Pydantic AI**: The current on-call engineer for the team that owns Project Helios is Kevin Nakamura, who is the On-Call Primary for the Payments Engineering team as of January 2025 [Source: team_directory.md].
- **LangGraph**: The current on-call engineer for the Payments Engineering team, which owns Project Helios, is Kevin Nakamura (as of 2025-01) [team_directory.md].
- **smolagents**: The current on-call engineer for the team that owns Project Helios is Kevin Nakamura. Source: team_directory.md

### q5: What was the root cause of the most recent incident that affected the server running Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 7.91 | 7.41 | 37.88 |
| Tokens | 1,840 | 4,317 | 25,378 |
| Correctness | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 0.67 | 0.67 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Chain Success | 1 | 1 | 1 |
| Grounded Hop Coverage | 1 | 1 | 1 |
| Hop Coverage | 1 | 1 | 1 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 3 | 3 | 3 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The most recent incident affecting the server running Project Aurora (prod-api-03) was INC-2025-042, which occurred on January 8, 2025. The root cause of this incident was a firmware bug in the top-of-rack switch (Arista 7280R3) that caused a spanning tree reconvergence event, resulting in a network...
- **LangGraph**: The root cause of the most recent incident affecting the server running Project Aurora (prod-api-03) was a firmware bug in the top-of-rack switch (Arista 7280R3). This bug caused a spanning tree reconvergence event, resulting in a network partition between racks R-400 through R-420, which dropped tr...
- **smolagents**: The root cause of the most recent incident affecting the server running Project Aurora (prod-api-03) was a firmware bug in the top-of-rack switch (Arista 7280R3), which caused a spanning tree reconvergence event, resulting in a network partition between racks R-400 through R-420. The incident was re...

### q6: What SLA tier applies to datacenters in the us-west region, and what is its uptime guarantee?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 6.70 | 8.66 | 34.84 |
| Tokens | 1,296 | 2,322 | 23,109 |
| Correctness | 5 | 3 | 5 |
| Completeness | 5 | 4 | 5 |
| Faithfulness | 5 | 4 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 0.50 | 0.50 |
| Chain Success | 1 | 0 | 1 |
| Grounded Hop Coverage | 1 | 0.333 | 0.667 |
| Hop Coverage | 1 | 0.667 | 1 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 3 | 2 | 3 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The SLA tier that applies to datacenters in the us-west region is the Gold tier. Its uptime guarantee is 99.95%, which equates to a maximum of 21.6 minutes of downtime per month (source: sla_policies.md).
- **LangGraph**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.9% (≤ 43.2 minutes downtime per month) according to the source document "sla_policies.md."
- **smolagents**: The SLA tier that applies to datacenters in the us-west region is the Gold tier, which has an uptime guarantee of 99.95% (≤ 21.6 minutes downtime per month). Source: sla_policies.md

### q7: What is the uptime guarantee for the server hosting Project Aurora?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 4.83 | 7.54 | 35.99 |
| Tokens | 1,397 | 3,611 | 28,681 |
| Correctness | 5 | 2 | 5 |
| Completeness | 3 | 2 | 5 |
| Faithfulness | 5 | 3 | 5 |
| Retrieval Prec | 0.67 | 1.00 | 1.00 |
| Retrieval Recall | 0.67 | 1.00 | 0.67 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0.333 | 0 | 0.667 |
| Hop Coverage | 0.333 | 0 | 0.667 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 1 | 0 | 2 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The uptime guarantee for the server hosting Project Aurora, which is the customer analytics platform, is 99.95% as specified under the Gold Tier service level agreement (SLA) [source: sla_policies.md].
- **LangGraph**: The uptime guarantee for the server hosting Project Aurora is not specified in the provided context. The SLA policies mention different tiers (Gold, Silver, Platinum) with their respective uptime guarantees, but the specific tier applicable to the server hosting Project Aurora is not indicated. Ther...
- **smolagents**: Based on the iterative retrieval process, here is the final answer to the question regarding the uptime guarantee for the server hosting Project Aurora:

The server hosting Project Aurora, identified as `prod-api-03`, is associated with the Gold tier of the Service Level Agreement (SLA). The Gold ti...

### q8: Which engineer should be contacted about the network partition incident that occurred at the Portland datacenter?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 10.68 | 8.20 | 41.35 |
| Tokens | 2,266 | 3,722 | 29,083 |
| Correctness | 2 | 1 | 5 |
| Completeness | 2 | 1 | 5 |
| Faithfulness | 3 | 3 | 5 |
| Retrieval Prec | 0.67 | 0.67 | 0.67 |
| Retrieval Recall | 0.67 | 0.67 | 0.67 |
| Chain Success | 0 | 0 | 0 |
| Grounded Hop Coverage | 0 | 0 | 0.667 |
| Hop Coverage | 0 | 0 | 0.667 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 0 | 0 | 2 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The network partition incident at the Portland datacenter is related to the network engineering team, which handled the application of the emergency firmware patch. However, the records do not specify a direct contact engineer for this incident. To follow the escalation path related to similar incid...
- **LangGraph**: The context does not provide specific names or contact information for engineers involved in the network partition incident at the Portland datacenter. It only mentions that the resolution was handled by the network engineering team. Therefore, I cannot specify which engineer should be contacted.
- **smolagents**: Based on the information retrieved, the engineer to contact regarding the network partition incident at the Portland datacenter is **Priya Patel**, who is the on-call primary for the Platform Infrastructure team. 

Here are the details:

- **Incident**: Network Partition in Portland Datacenter (INC-...

### q9: What is the maximum incident response time for P1 incidents affecting Project Helios, given its server's datacenter location?

| Metric | Pydantic AI | LangGraph | smolagents |
| --- | --- | --- | --- |
| Latency (s) | 10.05 | 6.38 | 34.07 |
| Tokens | 3,179 | 4,032 | 28,481 |
| Correctness | 5 | 5 | 5 |
| Completeness | 4 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 |
| Retrieval Prec | 0.75 | 0.75 | 0.75 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 |
| Chain Success | 0 | 1 | 1 |
| Grounded Hop Coverage | 0.667 | 1 | 1 |
| Hop Coverage | 0.667 | 1 | 1 |
| Is Multi Hop | 1 | 1 | 1 |
| Matched Hops | 2 | 3 | 3 |
| Required Hops | 3 | 3 | 3 |

**Answers:**

- **Pydantic AI**: The maximum incident response time for P1 incidents affecting Project Helios, which is hosted in the us-east region datacenters, is 15 minutes. This is based on the SLA policies that specify a response time of 15 minutes for P1 incidents in that region (as noted in the source document **sla_policies...
- **LangGraph**: The maximum incident response time for P1 incidents affecting Project Helios, which is hosted on the server prod-api-01 located in the us-east region datacenters, is 15 minutes. This is specified in the SLA policies document (sla_policies.md).
- **smolagents**: Based on the information retrieved, here is the answer to the question regarding the maximum incident response time for P1 incidents affecting Project Helios:

The maximum incident response time for P1 incidents affecting Project Helios is **15 minutes**. This is specified in the Service Level Agree...
