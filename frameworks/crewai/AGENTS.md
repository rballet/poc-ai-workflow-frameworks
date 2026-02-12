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

## Notes
- Model specified as `"openai/gpt-5-mini"` (LiteLLM provider/model format)
- `crew.akickoff()` does NOT exist in v1.6.1 — use `crew.kickoff_async()` instead
- `result.token_usage` is a Pydantic `UsageMetrics` model (NOT a dict) — use attribute access
- Agent initialized lazily via `_ensure_agent()`
- New Task + Crew created per query (Task description varies per question)
- `verbose=False` on both Agent and Crew to suppress internal logging
- Set `CREWAI_TRACING_ENABLED=false` to avoid interactive tracing prompt
- Higher token usage than other frameworks due to CrewAI's internal agent system prompts
