# Pydantic AI Implementation

Framework: Pydantic AI 1.56.0
Dependencies: pydantic-ai, chromadb, openai

## RAG QA Architecture (`rag_qa.py`)
Uses a Pydantic AI `Agent` with a `@agent.tool` for retrieval:
1. Agent receives the question and uses the `retrieve` tool
2. Tool embeds the query, searches chromadb, returns formatted chunks
3. Agent generates answer based on retrieved context

### Key APIs
- `Agent` from `pydantic_ai` — created lazily via `_build_agent()` to avoid import-time API key checks
- `RunContext[Deps]` — first parameter of `@agent.tool`, invisible to the LLM
- `result.usage()` returns `RunUsage` with `input_tokens`, `output_tokens`, `total_tokens`
- `result.all_messages()` for extracting source information from tool responses

## Agentic SQL Architecture (`agentic_sql_qa.py`)
Uses native Pydantic AI tool-calling with `Agent` and typed dependencies:
1. **Agent** with `deps_type=AgentDeps` holds the `AgenticSQLRuntime`
2. **Tools** — `run_sql` and `lookup_doc` as plain async functions taking `RunContext[AgentDeps]`
3. **Loop** — Pydantic AI's built-in agent loop handles tool calls automatically

### Key APIs
- `Agent(model, tools=[...], deps_type=AgentDeps)` for declarative tool registration
- `RunContext[AgentDeps]` gives tools access to the shared runtime
- `AgenticSQLRuntime` from `shared.agentic_sql` for shared tool logic

## Notes
- Agent initialization deferred to first use (`_ensure_agent()`)
- Model specified as `"openai:gpt-5-mini"` (Pydantic AI format)
- Token fields: `input_tokens`/`output_tokens` (not `prompt_tokens`/`completion_tokens`)
