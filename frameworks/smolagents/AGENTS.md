# smolagents Implementation

Framework: smolagents 1.24.0
Dependencies: smolagents, chromadb, openai

## Architecture
Uses a `CodeAgent` with a custom `RetrieverTool`:
1. `RetrieverTool` subclasses `smolagents.Tool` with `name`, `description`, `inputs`, `output_type`
2. `CodeAgent` writes Python code to call the tool and formulate an answer
3. Sync-only execution wrapped with `asyncio.to_thread()` for async compatibility

## Key APIs
- `Tool` base class — requires `name`, `description`, `inputs` dict, `output_type`, and `forward()` method
- `CodeAgent` from `smolagents` — uses `LiteLLMModel` for OpenAI access
- `agent.run(question, return_full_result=True)` returns `RunResult` with `token_usage` and `output`
- `agent.memory.steps` for extracting source information from observations

## Notes
- smolagents is **sync-only** — uses `asyncio.to_thread()` to bridge to async
- Model ID format: `"openai/gpt-4o-mini"` (LiteLLM convention)
- Agent recreated per query (stateless design)
- `verbosity_level=0` to suppress console output during benchmarks
