# POC: AI Workflow Frameworks Benchmark

## Overview
Benchmarks AI agent/workflow frameworks on identical scenarios to compare latency, cost, quality, and developer experience.

Frameworks: LangGraph 1.0.8, Pydantic AI 1.56.0, smolagents 1.24.0
Current scenarios: RAG Q&A, Multi-hop Q&A

## Tech Stack
- Python >= 3.12, package manager: uv (workspace mode)
- Vector store: chromadb (in-memory)
- Embeddings: OpenAI text-embedding-3-small
- LLM: gpt-4o-mini (default)
- Evaluation: custom harness with LLM-as-judge (gpt-4o-mini)

## Project Structure
- `shared-lib/` — Core interfaces, eval harness, reporting (Python package name: `shared`)
- `scenarios/` — Test scenarios with documents and questions (framework-agnostic)
- `frameworks/` — One subdir per framework, each is a uv workspace member
- `scripts/` — CLI entry points for running evals and comparisons
- `results/` — Generated output (gitignored except .gitkeep)

## Build & Run
```bash
uv sync --all-packages                                                # install all
uv run python scripts/run_eval.py --framework pydantic_ai --scenario rag_qa  # one framework
uv run python scripts/run_eval.py --all --scenario rag_qa                    # all frameworks
uv run python scripts/compare.py results/*.json                              # compare
```

## Key Conventions
- Every framework implements the `RAGFramework` Protocol from `shared.interface`
- Framework implementations MUST NOT import from other framework packages
- All LLM calls MUST populate UsageStats (tokens, latency, model name)
- Use `async def` for all interface methods
- Test documents are small markdown files in `scenarios/*/documents/`
- Scenario specs support `modes.baseline` and `modes.capability` for fair-vs-capability runs
- Scenario-specific evaluation logic is configured via `spec.yaml -> evaluation.profile`

## Environment Variables
- `OPENAI_API_KEY` — Required for embeddings and LLM calls
- `ANTHROPIC_API_KEY` — Required if using Claude models
- `HF_TOKEN` — Optional, for smolagents with HF Inference API
