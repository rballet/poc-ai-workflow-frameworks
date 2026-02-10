# Framework Implementations

Each subdirectory implements the `RAGFramework` Protocol for one framework.

## Rules
- Each framework is a separate uv workspace member with its own `pyproject.toml`.
- Depend on `shared` via `{ workspace = true }` in `[tool.uv.sources]`.
- Implement all methods of the `RAGFramework` Protocol from `shared.interface`.
- Optionally implement `configure(...)` (from `ConfigurableFramework`) for mode-aware runs.
- Track token usage and latency in every `query()` call.
- Use chromadb for vector storage (in-memory mode).
- Each implementation MUST work independently — no cross-framework imports.

## Common Pattern
Each `rag_qa.py` should:
1. **ingest()**: Chunk documents, embed with OpenAI, store in chromadb
2. **query()**: Embed the question, retrieve top-k chunks, call LLM with context, return `RunResult`
3. **cleanup()**: Delete the chromadb collection

Mode-aware behavior:
- `baseline` mode should preserve fair, minimal retrieval pipelines.
- `capability` mode may use iterative/planned retrieval under scenario budget constraints.

## Adding a New Framework
1. Create `frameworks/<name>/` with `pyproject.toml` and `src/impl_<name>/`
2. Add it as a workspace member in root `pyproject.toml`
3. Implement `RAGFramework` protocol in `src/impl_<name>/rag_qa.py`
4. Register it in `scripts/run_eval.py` `get_framework()` function
5. Run `uv sync --all-packages`
