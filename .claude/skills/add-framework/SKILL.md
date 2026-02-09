---
name: add-framework
description: >
  Scaffold a new framework implementation for the benchmark. Use when the user wants to
  add a new AI agent framework to the comparison. Creates directory structure, pyproject.toml,
  AGENTS.md, and a skeleton implementation of the RAGFramework Protocol.
---

# Add Framework

## When to use
Use when the user wants to add a new AI framework to the benchmark comparison.

## Steps

1. Create directory structure:
   ```
   frameworks/<name>/
   ├── AGENTS.md
   ├── pyproject.toml
   └── src/impl_<name>/
       ├── __init__.py
       └── rag_qa.py
   ```

2. Create `pyproject.toml`:
   ```toml
   [project]
   name = "impl-<name>"
   version = "0.1.0"
   requires-python = ">=3.12"
   dependencies = [
       "<framework-package>",
       "chromadb>=0.5",
       "openai>=1.0",
       "shared",
   ]

   [tool.uv.sources]
   shared = { workspace = true }

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

   [tool.hatch.build.targets.wheel]
   packages = ["src/impl_<name>"]
   ```

3. Add to root `pyproject.toml` workspace members:
   ```toml
   [tool.uv.workspace]
   members = [
       ...,
       "frameworks/<name>",
   ]
   ```

4. Create skeleton `rag_qa.py` implementing `RAGFramework` Protocol:
   - `name` property returning the framework name
   - `async ingest(documents)` — chunk, embed, store in chromadb
   - `async query(question)` — retrieve, generate, return RunResult with UsageStats
   - `async cleanup()` — delete chromadb collection

5. Register in `scripts/run_eval.py` `get_framework()`:
   ```python
   elif name == "<name>":
       from impl_<name>.rag_qa import <ClassName>
       return <ClassName>()
   ```

6. Add to `FRAMEWORKS` list in `scripts/run_eval.py`

7. Write `AGENTS.md` documenting the framework's architecture and key APIs

8. Install: `uv sync --all-packages`

## Important
- Always research the framework's latest docs before implementing
- Use the same embedding model and chromadb pattern as existing implementations
- Track token usage in UsageStats
