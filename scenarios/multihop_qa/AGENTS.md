# Multi-hop QA Scenario

Multi-hop RAG Q&A requiring fact-chaining across multiple documents.

## Overview
- Scenario type: `rag_qa`
- Profile: `multihop_chain_qa` (hop coverage and grounded hop coverage metrics)
- Questions require combining facts from 2+ documents to reach the answer

## Assets
- `spec.yaml` — scenario config with baseline/capability budgets
- `questions.yaml` — multi-hop questions with expected hops metadata
- `documents/` — interconnected technical documents (DevOps infrastructure)

## Configuration (spec.yaml)
- Embedding: `text-embedding-3-small`
- LLM: `gpt-5-mini`
- Chunk size: 500 chars, 50 overlap
- Top-K retrieval: 3 chunks
- Capability mode adds iterative retrieval rounds and follow-up queries
