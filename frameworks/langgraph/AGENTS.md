# LangGraph Implementation

Framework: LangGraph 1.0.8
Dependencies: langgraph, langchain-openai, langchain-community, chromadb

## RAG QA Architecture (`rag_qa.py`)
Uses a `StateGraph` with two nodes in a linear pipeline:
1. **retrieve** — Embeds the question, queries chromadb for top-k chunks
2. **generate** — Calls `ChatOpenAI` with retrieved context + system prompt

### Key APIs
- `StateGraph`, `START`, `END` from `langgraph.graph`
- `ChatOpenAI` from `langchain_openai` for LLM calls
- `response.usage_metadata` for token counts (`input_tokens`, `output_tokens`)
- Graph compiled with `workflow.compile()`, invoked with `graph.ainvoke()`

### State Schema
`RAGState(TypedDict)` with fields: `question`, `context_chunks`, `context_sources`, `answer`, `input_tokens`, `output_tokens`

## Agentic SQL Architecture (`agentic_sql_qa.py`)
Uses native LangGraph tool-calling with a prebuilt agent loop:
1. **agent** — `ChatOpenAI.bind_tools()` decides next action
2. **tools** — `ToolNode` executes `run_sql` / `lookup_doc` via `AgenticSQLRuntime`
3. **routing** — `tools_condition` auto-routes between tool calls and `END`

### Key APIs
- `MessagesState` from `langgraph.graph` (built-in message list state)
- `ToolNode`, `tools_condition` from `langgraph.prebuilt`
- `@tool` decorator from `langchain_core.tools`
- `llm.bind_tools([...])` for native function calling
- `AgenticSQLRuntime` from `shared.agentic_sql` for shared tool logic
