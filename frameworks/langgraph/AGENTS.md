# LangGraph Implementation

Framework: LangGraph 1.0.8
Dependencies: langgraph, langchain-openai, langchain-community, chromadb

## Architecture
Uses a `StateGraph` with two nodes in a linear pipeline:
1. **retrieve** — Embeds the question, queries chromadb for top-k chunks
2. **generate** — Calls `ChatOpenAI` with retrieved context + system prompt

## Key APIs
- `StateGraph`, `START`, `END` from `langgraph.graph`
- `ChatOpenAI` from `langchain_openai` for LLM calls
- `response.usage_metadata` for token counts (`input_tokens`, `output_tokens`)
- Graph compiled with `workflow.compile()`, invoked with `graph.ainvoke()`

## State Schema
`RAGState(TypedDict)` with fields: `question`, `context_chunks`, `context_sources`, `answer`, `input_tokens`, `output_tokens`
