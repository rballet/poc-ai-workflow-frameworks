# POC: AI Workflow Frameworks Benchmark

Comparing AI agent frameworks by running **identical scenarios** through each one and measuring what matters: latency, cost, answer quality, retrieval accuracy, and implementation code quality.

## Frameworks

| Framework | Version | Notes |
|---|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | >=1.0 | Graph-based state machine from LangChain |
| [Pydantic AI](https://ai.pydantic.dev/) | >=1.0 | Type-safe agents from the Pydantic team |
| [smolagents](https://huggingface.co/docs/smolagents) | >=1.0 | Lightweight agents from Hugging Face |

## Quick Start

```bash
# Prerequisites: Python 3.12+, uv
uv sync --all-packages

# Set up API keys
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run one framework
uv run python scripts/run_eval.py --framework pydantic_ai --scenario rag_qa

# Run all frameworks
uv run python scripts/run_eval.py --all --scenario rag_qa

# Run capability mode (iterative retrieval + scenario profile metrics)
uv run python scripts/run_eval.py --all --scenario multihop_qa --mode capability

# Run without LLM code review (faster, no extra API cost)
uv run python scripts/run_eval.py --all --scenario rag_qa --skip-code-review

# Disable shared embedding store (each framework embeds independently)
uv run python scripts/run_eval.py --all --scenario rag_qa --no-shared-store

# Compare results
uv run python scripts/compare.py results/*.json -o results/comparison.md
```

## Repository Structure

```
.
├── shared-lib/              # Framework-agnostic interface and evaluation engine
│   └── src/shared/
│       ├── interface.py     # RAGFramework Protocol — the contract all frameworks implement
│       ├── scenario.py      # Scenario loader + normalized scenario metadata
│       ├── retrieval.py     # Shared embedding store with query caching
│       ├── retrieval_strategy.py # Baseline/capability retrieval strategies
│       └── eval/
│           ├── harness.py      # Orchestrates ingest → query → judge → aggregate
│           ├── profiles.py     # Scenario-specific quality metrics
│           ├── llm_judge.py    # LLM-as-judge scoring (correctness, completeness, faithfulness)
│           ├── code_quality.py # Static metrics via radon + ast
│           ├── code_review.py  # LLM-as-judge code review (readability, extensibility, …)
│           ├── metrics.py      # Token cost estimation
│           └── retrieval.py    # Precision and recall on retrieved sources
│
├── frameworks/              # One implementation per framework, same interface
│   ├── langgraph/
│   ├── pydantic_ai/
│   └── smolagents/
│
├── scenarios/               # Test scenarios with documents + questions
│   └── rag_qa/              # Simple RAG Q&A over technical docs
│       ├── spec.yaml        # Scenario config (model, chunk size, top-k)
│       ├── questions.yaml   # Questions with expected answers and sources
│       └── documents/       # Source documents (Python, HTTP, Git)
│
├── scripts/
│   ├── run_eval.py          # CLI to run benchmarks
│   └── compare.py           # CLI to generate comparison reports
│
└── results/                 # Output JSON + markdown reports (git-ignored)
```

## How It Works

Every framework implements the same `RAGFramework` Protocol:

```python
class RAGFramework(Protocol):
    @property
    def name(self) -> str: ...
    async def ingest(self, documents: list[Document]) -> None: ...
    async def query(self, question: str) -> RunResult: ...
    async def cleanup(self) -> None: ...
```

Frameworks can optionally implement `ConfigurableFramework.configure(...)` to adapt behavior by scenario mode (`baseline` vs `capability`) without changing the base protocol.

The evaluation harness feeds the same documents and questions to each implementation, then collects metrics through a shared pipeline. See [METRICS.md](METRICS.md) for details on what is measured and how.

## Design Principles

- **Two-track evaluation** — run `baseline` mode for strict parity and `capability` mode for framework-tuned strategies under the same scenario budget.
- **Fair baseline** — shared embedding store and aligned defaults keep baseline runs comparable.
- **Extensible scenario profiles** — scenario-specific quality metrics are plug-ins (e.g., multi-hop chain/hop coverage).
- **Framework-agnostic scenarios** — scenarios are defined as YAML + documents. Any framework that satisfies the Protocol can run them.
- **Code quality analysis** — each framework's implementation is evaluated for complexity, maintainability, and coding standards via static analysis (radon) and LLM-as-judge code review.
- **Extensible** — add frameworks, scenario types, and profile metrics without changing the core harness.

## Adding a Framework

1. Create `frameworks/<name>/` with a `pyproject.toml` depending on `shared`
2. Implement a class satisfying `RAGFramework` in `src/impl_<name>/rag_qa.py`
3. Optionally implement `configure(...)` for mode-aware capability behavior
4. Register it in `scripts/run_eval.py` → `get_framework()`
5. Add the workspace member to the root `pyproject.toml`

## Adding a Scenario

1. Create `scenarios/<name>/` with `spec.yaml`, `questions.yaml`, and a `documents/` folder
2. Set `scenario_type`, `evaluation.profile`, and optional `modes.baseline/capability` in `spec.yaml`
3. For complex tasks, add per-question `metadata` (e.g., required hops, tool expectations)
4. Follow the structure of `scenarios/rag_qa/` as a template
5. Reference the new scenario name with `--scenario <name>`

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key (for embeddings + LLM + judge)
