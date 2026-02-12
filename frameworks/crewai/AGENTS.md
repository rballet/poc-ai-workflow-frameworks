# CrewAI Implementation

Framework: CrewAI 1.6.1
Dependencies: crewai, chromadb, openai

## RAG QA Architecture (`rag_qa.py`)
Uses a CrewAI Agent/Task/Crew with a fixed retrieve-then-generate pipeline:
1. Retrieve top-k chunks from shared EmbeddingStore (or local chromadb)
2. Create a Task with context + question as the description
3. Run a single-agent Crew to generate the answer
4. Extract token usage from CrewOutput.token_usage

### Key APIs
- `LLM(model="openai/gpt-5-mini")` — CrewAI LLM wrapper (uses LiteLLM internally)
- `Agent(role, goal, backstory, llm, verbose)` — defines an AI agent
- `Task(description, expected_output, agent)` — defines a unit of work
- `Crew(agents, tasks, verbose)` — orchestrates agent execution
- `await crew.kickoff_async()` — async execution (thread-based wrapper around sync kickoff)
- `crew_output.raw` — string answer
- `crew_output.token_usage` — `UsageMetrics` pydantic model with `.prompt_tokens`, `.completion_tokens`, `.total_tokens`

## Multihop QA Architecture (`multihop_qa.py`)
Uses three specialized agents for iterative retrieval with planning and validation:
1. **Planner Agent** — generates retrieval subqueries for multi-hop questions (returns JSON)
2. **Answer Agent** — generates answers from retrieved context
3. **Checker Agent** — validates answer sufficiency and suggests follow-up queries (returns JSON)

### Baseline mode
Single retrieval pass + single answer Crew run.

### Capability mode
1. Planner Crew → parse subqueries from JSON output
2. Retrieve for each planned subquery
3. Answer Crew → draft answer
4. Checker Crew → assess sufficiency, get missing queries
5. If not sufficient: retrieve missing queries → final Answer Crew

## Agentic SQL QA Architecture (`agentic_sql_qa.py`)
Uses CrewAI's native tool-calling with two custom tools:
1. **RunSQLTool** — extends `BaseTool`, delegates to `AgenticSQLRuntime.run_sql()`
2. **LookupDocTool** — extends `BaseTool`, delegates to `AgenticSQLRuntime.lookup_doc()`

### Key patterns
- Tools extend `crewai.tools.BaseTool` with `_run()` method and `args_schema` (Pydantic model)
- `model_config = {"arbitrary_types_allowed": True}` required for non-serializable runtime refs
- `Agent(max_iter=max_steps+2)` controls iteration budget; runtime enforces `max_tool_calls`
- Tools instantiated per query (runtime.start_run resets state each time)

## Notes
- Model specified as `"openai/gpt-5-mini"` (LiteLLM provider/model format)
- `crew.akickoff()` does NOT exist in v1.6.1 — use `crew.kickoff_async()` instead
- `result.token_usage` is a Pydantic `UsageMetrics` model (NOT a dict) — use attribute access
- Agent initialized lazily via `_ensure_agent()`
- New Task + Crew created per query (Task description varies per question)
- `verbose=False` on both Agent and Crew to suppress internal logging
- Set `CREWAI_TRACING_ENABLED=false` to avoid interactive tracing prompt
- Higher token usage than other frameworks due to CrewAI's internal agent system prompts
