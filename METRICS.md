# Metrics

How frameworks are evaluated and what each metric means.

## Overview

Each framework runs the same set of questions against the same documents. Per-question results are collected, then aggregated into a framework-level summary. The evaluation has three layers: **performance**, **answer quality**, and **retrieval quality**.

## Performance Metrics

| Metric | Unit | Source |
|---|---|---|
| **Latency** | seconds | Wall-clock time per question (embed + retrieve + generate) |
| **Prompt tokens** | count | Reported by the LLM provider |
| **Completion tokens** | count | Reported by the LLM provider |
| **Total tokens** | count | Prompt + completion |
| **Estimated cost** | USD | Computed from token counts using a per-model pricing table |

Cost estimation normalizes model name variants (e.g. `openai/gpt-5-mini` and `gpt-5-mini` resolve to the same pricing). Unknown models report $0.

### Timeout Guardrail

Each question run is protected by a configurable timeout (`--query-timeout-seconds`, default `120`).

- On timeout, the framework answer is marked as timed out and scoring is set to 0 for that question.
- This prevents one slow/looping question from blocking the entire benchmark run.

## Answer Quality — LLM-as-Judge

An independent LLM (default: `gpt-5-mini`) scores each answer on three criteria. It receives the question, expected answer, actual answer, and retrieved sources.

| Criterion | Scale | What it measures |
|---|---|---|
| **Correctness** | 1–5 | Is the answer factually accurate relative to the expected answer? |
| **Completeness** | 1–5 | Does it cover all key points from the expected answer? |
| **Faithfulness** | 1–5 | Is it grounded in the retrieved sources (no hallucination)? |

The judge also returns free-text **reasoning** explaining each score.

### Scoring Guidelines

| Score | Meaning |
|---|---|
| 5 | Excellent — fully correct/complete/faithful |
| 4 | Good — minor omissions or imprecisions |
| 3 | Acceptable — partially correct, missing key details |
| 2 | Poor — significant errors or gaps |
| 1 | Bad — wrong, empty, or entirely unsupported by sources |

## Retrieval Quality

Measured by comparing the sources the framework retrieved against the expected sources defined in `questions.yaml`.

| Metric | Range | Formula |
|---|---|---|
| **Precision** | 0–1 | (relevant retrieved) / (total retrieved) |
| **Recall** | 0–1 | (relevant retrieved) / (total relevant) |

High precision = the framework isn't pulling in irrelevant documents.
High recall = it's finding all the documents it should.

## Code Quality — Static Analysis

Unlike the metrics above (which are per-question), code quality is evaluated **once per framework** on its implementation source file. These metrics are deterministic and require no LLM calls.

Powered by [radon](https://radon.readthedocs.io/) and Python's `ast` module.

| Metric | Unit | What it measures |
|---|---|---|
| **SLOC** | count | Source lines of code (excludes blanks and comments) |
| **Comment Ratio** | 0–1 | Comment lines / SLOC |
| **Avg Cyclomatic Complexity** | float | Mean number of independent code paths per function |
| **Max Cyclomatic Complexity** | int | Highest CC across all functions in the file |
| **Complexity Grade** | A–F | Radon letter grade based on average CC |
| **Maintainability Index** | 0–100 | Composite of LOC, CC, and Halstead volume. Higher = easier to maintain |
| **Maintainability Grade** | A/B/C | A (>=20), B (10–19), C (<10) |
| **Halstead Volume** | float | Information content of the code (operand/operator vocabulary) |
| **Halstead Difficulty** | float | How hard the code is to write or understand |
| **Halstead Bugs (est.)** | float | Estimated number of bugs (volume / 3000) |
| **Total Imports** | count | All `import` / `from ... import` statements |
| **Framework Imports** | count | Imports from framework-specific packages |
| **Classes** | count | Number of class definitions |
| **Functions** | count | Number of function/method definitions |
| **Type Annotation Coverage** | 0–1 | Fraction of functions with return type annotations |

### Interpreting Maintainability Index

| Grade | Range | Meaning |
|---|---|---|
| A | 20–100 | Easy to maintain |
| B | 10–19 | Moderate effort to maintain |
| C | 0–9 | Difficult to maintain |

## Code Quality — LLM Code Review

An independent LLM (default: `gpt-5-mini`) reviews each framework's source code and scores it on seven criteria. It receives the framework name, scenario description, and full source code.

| Criterion | Scale | What it measures |
|---|---|---|
| **Readability** | 1–5 | Naming, formatting, logical flow, cognitive load |
| **Idiomatic Usage** | 1–5 | Correct use of the framework's APIs and Python idioms |
| **Error Handling** | 1–5 | Robustness with edge cases, exceptions, invalid states |
| **Extensibility** | 1–5 | Ease of adding new features without major refactoring |
| **Testability** | 1–5 | Component isolation, mockability, unit test feasibility |
| **Documentation** | 1–5 | Docstrings, comments, self-documenting code |
| **Abstraction** | 1–5 | Appropriate level — not over-engineered, not too flat |

The reviewer also returns free-text **reasoning**. Uses `temperature=0` for consistency, though minor variance between runs is possible.

Use `--skip-code-review` to skip the LLM review (static analysis only, no API cost).
Use `--skip-code-quality` to skip all code quality evaluation.

## Aggregation

Framework-level summaries are simple averages across all questions, except:
- **Total tokens** and **total cost** are summed (not averaged)
- **Code quality** is evaluated once per framework, not aggregated from per-question data

## Comparison Report Metrics

The markdown report generated by `scripts/compare.py` includes additional cross-framework views:

- **Runtime distribution**
  - `Latency p50`
  - `Latency p95`
- **Derived scorecard (0-100)**
  - `Capability` (quality + scenario-specific capability signals)
  - `Efficiency` (latency, cost, and token footprint)
  - `Developer Experience` (static metrics + optional LLM code review signals)

These are decision aids and should not replace direct inspection of raw quality, latency, and per-question results.

## Controlling Variables

To ensure a fair comparison, all frameworks share core parameters per scenario. Values are set in each scenario's `spec.yaml`.

### Shared across all scenarios

| Parameter | Value | Set in |
|---|---|---|
| LLM model | `gpt-5-mini` | Each `spec.yaml` |
| Embedding model | `text-embedding-3-small` | Each `spec.yaml` |
| Temperature | `0` | Each framework implementation |
| System prompt | Identical across all three | Each framework implementation |
| Chunk size | 500 chars | Each `spec.yaml` |
| Chunk overlap | 50 chars | Each `spec.yaml` |

### Scenario-specific parameters

| Parameter | RAG QA | Multi-hop QA | Agentic SQL QA | Multi-Agent Coordination |
|---|---|---|---|---|
| Top-k retrieval | 3 | 3 | 4 | 4 |
| Database seed file | — | — | `data/seed.sql` | `data/seed.sql` |
| Capability max_steps | — | 4 | 10 | 15 |
| Capability max_tool_calls | — | — | 10 | 30 |

## Multi-Run Averaging (`--runs N`)

When `--runs N` is used with N > 1, the harness evaluates each framework N times and produces an averaged result:

- Per-question scores (correctness, completeness, faithfulness, retrieval precision/recall, latency) are averaged across runs.
- Token counts and cost are summed across runs.
- A representative answer (closest to mean correctness) is selected for each question.
- Per-question `correctness_stddev` and run-level `correctness_run_stddev`, `completeness_run_stddev`, `faithfulness_run_stddev` are tracked.
- Individual run results are saved alongside the aggregated file (e.g. `_run1.json`, `_run2.json`).
- The comparison report shows `±stddev` notation when run_count > 1.

This is useful because GPT-5-mini (and GPT-5 family reasoning models) do not support `temperature=0`, making results inherently non-deterministic.

## Output Format

Results are saved as JSON files in `results/`, one per run:

```
results/langgraph_rag_qa_20260209_174417.json
results/pydantic_ai_rag_qa_20260209_174352.json
results/smolagents_rag_qa_20260209_174446.json
```

Each file contains the full `FrameworkEvaluation`: per-question scores, aggregates, and metadata. The comparison script reads these files and produces a markdown report with summary tables and per-question breakdowns.

## Scenario Profile Extensions

Scenario profiles can add extra metrics via `shared.eval.profiles`:

- `default`: no extra metrics
- `multihop_chain_qa`: hop coverage and grounded hop coverage for multi-hop questions
- `tool_branching_qa`: separates easy vs branching questions and tracks:
  - branching hop coverage / success rate
  - grounded hop coverage on branching questions
  - tool coverage against expected tools (when tool traces are reported)
  - tool trace reporting rate
- `multi_agent_coordination`: separates easy vs coordination questions and tracks:
  - agent coverage (did the framework invoke the required specialist domains?)
  - coordination success rate (agent coverage + hop coverage threshold)
  - hop coverage and grounded hop coverage on coordination questions
  - tool coverage and tool trace reporting rate
