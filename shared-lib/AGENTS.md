# Shared Package

Core interfaces and evaluation harness used by all framework implementations.

## Key Files
- `src/shared/interface.py` — The `RAGFramework` Protocol. Every framework must satisfy this contract.
- `src/shared/eval/harness.py` — Evaluation runner (framework-agnostic). Orchestrates ingest, query, judge, and aggregate.
- `src/shared/eval/llm_judge.py` — LLM-as-judge scoring (correctness, completeness, faithfulness on 1-5 scale).
- `src/shared/eval/metrics.py` — Cost estimation from token counts per model.
- `src/shared/eval/retrieval.py` — Retrieval precision and recall.
- `src/shared/eval/profiles.py` — Scenario-specific metrics (e.g. multi-hop hop/chain coverage).
- `src/shared/scenario.py` — Scenario loading with normalized `scenario_type`, `modes`, and `evaluation.profile`.

## Rules
- This package MUST NOT depend on any framework-specific packages.
- Keep the Protocol minimal — only what is needed for evaluation.
- All quality scores use 1.0-5.0 (judge) or 0.0-1.0 (retrieval).
- The judge model defaults to `gpt-5-mini` for cost reasons.
- Keep scenario/profile plugins modular so new scenario types can be added without changing core harness logic.

## Build
```bash
uv sync --all-packages
```
