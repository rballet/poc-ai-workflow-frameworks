You are implementing new framework integrations for an AI benchmark project.

## Context Files

Study these files to understand the project:
- AGENTS.md — project overview, conventions, tech stack
- README.md — structure, protocol, how to add frameworks
- METRICS.md — what's measured, controlled variables
- prd.json — task list with completion status
- progress.txt — learnings from prior iterations

## Rules

1. Read prd.json — find the highest-priority story where `passes: false`
2. Read progress.txt — understand what was done in prior iterations and avoid repeating mistakes
3. Implement ONLY THAT ONE STORY — do not touch other stories
4. Follow the existing patterns exactly:
   - Use frameworks/pydantic_ai/ as the primary reference implementation
   - Use shared EmbeddingStore via constructor injection
   - All LLM calls must populate UsageStats (prompt_tokens, completion_tokens, total_tokens, latency_seconds, model_name)
   - Use `async def` for all interface methods
   - Support model override via `__init__(model=...)` parameter
5. Before writing code, research the framework's latest API using its official docs
6. Run verification after implementation:
   - `uv sync --all-packages`
   - `uv run python scripts/run_eval.py --framework <name> --scenario rag_qa --skip-code-review`
   - If the eval fails, read the error, fix it, and re-run. Do not mark the story as passing until the eval completes successfully.
7. After a successful run:
   - Update prd.json: set the story's `passes` to `true`
   - Append to progress.txt: what you implemented, files changed, learnings and gotchas discovered
   - Update the framework's AGENTS.md with discovered patterns and key APIs
   - Commit: `feat: add <framework> rag_qa implementation`
8. If ALL stories in prd.json have `passes: true`, output exactly:
   <promise>COMPLETE</promise>

## Critical Constraints

- Framework implementations MUST NOT import from other framework packages
- Use chromadb for vector storage when not using shared EmbeddingStore
- Use OpenAI text-embedding-3-small for embeddings when not using shared store
- Register new frameworks in scripts/run_eval.py in THREE places:
  1. `_FRAMEWORK_CLASS_NAMES` dict (maps framework key to class name)
  2. `FRAMEWORKS` list
  3. `_format_model_for_framework()` (add provider prefix logic if needed)
- Add the workspace member to root pyproject.toml
- The class name MUST be the one registered in `_FRAMEWORK_CLASS_NAMES`
- If uv sync fails with tiktoken/encoding errors: `rm -rf .venv && uv sync --all-packages`
