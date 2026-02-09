---
name: run-benchmark
description: >
  Run the benchmark evaluation for one or all framework implementations against a scenario.
  Use this skill when the user wants to execute benchmarks, run evaluations, or test
  a framework implementation. Handles execution and result collection.
---

# Run Benchmark

## When to use
Use when the user asks to run a benchmark, evaluate a framework, or test an implementation.

## Prerequisites
- `OPENAI_API_KEY` environment variable must be set
- All packages must be installed: `uv sync --all-packages`

## Steps

1. Verify environment:
   ```bash
   echo $OPENAI_API_KEY | head -c 8
   ```

2. Run for a single framework:
   ```bash
   uv run python scripts/run_eval.py --framework <name> --scenario rag_qa
   ```
   Valid framework names: `pydantic_ai`, `langgraph`, `smolagents`

3. Run for all frameworks:
   ```bash
   uv run python scripts/run_eval.py --all --scenario rag_qa
   ```

4. Results are saved to `results/<framework>_<scenario>_<timestamp>.json`

5. Generate comparison report:
   ```bash
   uv run python scripts/compare.py results/*.json -o results/comparison.md
   ```

## Troubleshooting
- If import errors occur, run `uv sync --all-packages` to reinstall
- If API errors occur, verify `OPENAI_API_KEY` is set and valid
- Each framework run takes ~30-60 seconds (7 questions + judge calls)
