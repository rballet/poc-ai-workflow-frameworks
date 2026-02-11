# smolagents Implementation

Framework: smolagents 1.24.0
Dependencies: smolagents, chromadb, openai

## RAG QA Architecture (`rag_qa.py`)
Uses `LiteLLMModel` with direct `litellm.completion()` calls:
1. Retrieval via shared `EmbeddingStore` or standalone chromadb
2. `litellm.completion()` with system prompt + context for generation
3. Sync-only execution wrapped with `asyncio.to_thread()` for async compatibility

## Agentic SQL Architecture (`agentic_sql_qa.py`)
Uses native smolagents tool-calling with `ToolCallingAgent`:
1. **Tools** — `SQLTool` and `DocTool` subclass `smolagents.Tool` with `forward()` delegating to `AgenticSQLRuntime`
2. **Agent** — `ToolCallingAgent` with `LiteLLMModel` handles tool selection and execution
3. **Loop** — smolagents' built-in agent loop manages tool calls, with optional `planning_interval`

### Key APIs
- `Tool` base class — requires `name`, `description`, `inputs` dict, `output_type`, and `forward()` method
- `ToolCallingAgent` from `smolagents` — uses `LiteLLMModel` for OpenAI access
- `agent.run(task, return_full_result=True)` returns `RunResult` with `token_usage` and `output`
- `AgenticSQLRuntime` from `shared.agentic_sql` for shared tool logic

## Notes
- smolagents is **sync-only** — uses `asyncio.to_thread()` to bridge to async
- Model ID format: `"openai/gpt-5-mini"` (LiteLLM convention)
- Agent recreated per query (stateless design)
- `verbosity_level=0` to suppress console output during benchmarks
