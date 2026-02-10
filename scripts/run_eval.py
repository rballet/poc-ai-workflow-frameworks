"""CLI entry point: run evaluation for one or all frameworks on a scenario."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import importlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # Load .env file from project root

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "shared-lib" / "src"))
for _framework in ("langgraph", "pydantic_ai", "smolagents"):
    sys.path.insert(0, str(ROOT / "frameworks" / _framework / "src"))

from shared.eval.harness import FrameworkEvaluation, evaluate_framework  # noqa: E402
from shared.eval.profiles import ProfileContext, get_scenario_profile  # noqa: E402
from shared.interface import ConfigurableFramework  # noqa: E402
from shared.retrieval import EmbeddingStore  # noqa: E402
from shared.scenario import (  # noqa: E402
    ScenarioDefinition,
    load_scenario as load_scenario_definition,
)

from compare import generate_comparison_report  # noqa: E402

SCENARIOS_DIR = ROOT / "scenarios"
RESULTS_DIR = ROOT / "results"


def load_scenario(scenario_name: str) -> ScenarioDefinition:
    """Load scenario assets and normalized metadata."""
    try:
        return load_scenario_definition(SCENARIOS_DIR, scenario_name)
    except FileNotFoundError as err:
        print(f"Error: {err}")
        sys.exit(1)


def create_embedding_store(scenario: ScenarioDefinition) -> EmbeddingStore:
    """Create and populate a shared EmbeddingStore from scenario config."""
    config = scenario.config
    store = EmbeddingStore(
        embedding_model=config.get("embedding_model", "text-embedding-3-small"),
        chunk_size=config.get("chunk_size", 500),
        chunk_overlap=config.get("chunk_overlap", 50),
        top_k=config.get("top_k", 3),
    )
    store.ingest(scenario.documents)
    return store


_FRAMEWORK_CLASS_NAMES = {
    "pydantic_ai": "PydanticAIRAG",
    "langgraph": "LangGraphRAG",
    "smolagents": "SmolAgentsRAG",
}


def get_framework(
    name: str,
    scenario_name: str,
    embedding_store: EmbeddingStore | None = None,
):
    """Import and instantiate a framework by name.

    Tries a scenario-specific implementation first (e.g. ``multihop_qa.py``),
    then falls back to ``rag_qa.py``.
    """
    if name not in _FRAMEWORK_CLASS_NAMES:
        print(f"Error: unknown framework '{name}'")
        sys.exit(1)

    class_name = _FRAMEWORK_CLASS_NAMES[name]
    import_errors: list[str] = []
    for module_suffix in [scenario_name, "rag_qa"]:
        module_name = f"impl_{name}.{module_suffix}"
        try:
            module = importlib.import_module(module_name)
            framework_cls = getattr(module, class_name)
            return framework_cls(embedding_store=embedding_store)
        except ModuleNotFoundError as err:
            # If an internal dependency is missing, surface it immediately.
            if err.name and not module_name.startswith(err.name):
                raise
            import_errors.append(f"{module_name}: {err}")
        except AttributeError as err:
            import_errors.append(f"{module_name}: {err}")

    print(f"Error: no implementation found for framework '{name}' and scenario '{scenario_name}'")
    for err in import_errors:
        print(f"  - {err}")
    sys.exit(1)


def get_framework_source(name: str, scenario: str) -> str | None:
    """Resolve framework source path (scenario-specific with rag_qa fallback)."""
    for candidate in [scenario, "rag_qa"]:
        source_path = ROOT / "frameworks" / name / "src" / f"impl_{name}" / f"{candidate}.py"
        if source_path.exists():
            return str(source_path)
    print(f"Warning: source file not found for framework '{name}' scenario '{scenario}'")
    return None


def save_results(evaluation: FrameworkEvaluation, output_dir: Path) -> Path:
    """Save evaluation results to JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{evaluation.framework_name.lower().replace(' ', '_')}_{evaluation.scenario_name}_{timestamp}.json"
    output_path = output_dir / filename

    data = dataclasses.asdict(evaluation)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    return output_path


def _print_extra_aggregates(extra_aggregates: dict[str, float]) -> None:
    for key, value in sorted(extra_aggregates.items()):
        value_str = str(int(value)) if abs(value - int(value)) < 1e-9 else f"{value:.3f}"
        print(f"  {key}:".ljust(24) + value_str)


async def run_single(
    framework_name: str,
    scenario: ScenarioDefinition,
    mode: str,
    judge_model: str,
    skip_code_quality: bool = False,
    skip_code_review: bool = False,
    embedding_store: EmbeddingStore | None = None,
) -> FrameworkEvaluation:
    """Run evaluation for a single framework."""
    framework = get_framework(
        framework_name,
        scenario_name=scenario.name,
        embedding_store=embedding_store,
    )
    mode_config = scenario.modes.get(mode, {})
    if isinstance(framework, ConfigurableFramework):
        framework.configure(
            mode=mode,
            scenario_name=scenario.name,
            scenario_type=scenario.scenario_type,
            scenario_config=scenario.config,
            mode_config=mode_config,
        )

    profile_key = scenario.evaluation.get("profile", "default")
    scenario_profile = get_scenario_profile(profile_key)
    profile_context = ProfileContext(
        scenario_name=scenario.name,
        scenario_type=scenario.scenario_type,
        mode=mode,
        profile_key=profile_key,
        profile_config=scenario.evaluation.get("profile_config", {}),
    )

    print(f"\n{'='*60}")
    print(f"Evaluating: {framework.name}")
    print(f"Scenario: {scenario.name} ({len(scenario.questions)} questions)")
    print(f"Mode: {mode} | Type: {scenario.scenario_type} | Profile: {profile_key}")
    print(f"{'='*60}")

    source_path = None
    if not skip_code_quality:
        source_path = get_framework_source(framework_name, scenario.name)

    evaluation = await evaluate_framework(
        framework=framework,
        documents=scenario.documents,
        questions=scenario.questions,
        scenario_name=scenario.name,
        scenario_type=scenario.scenario_type,
        evaluation_mode=mode,
        judge_model=judge_model,
        scenario_profile=scenario_profile,
        profile_context=profile_context,
        source_path=source_path,
        framework_key=framework_name,
        scenario_description=scenario.description,
        skip_code_review=skip_code_review,
    )

    print(f"\nResults for {evaluation.framework_name}:")
    print(f"  Avg Latency:           {evaluation.avg_latency:.2f}s")
    print(f"  Total Tokens:          {evaluation.total_tokens}")
    print(f"  Total Cost:            ${evaluation.total_cost_usd:.4f}")
    print(f"  Avg Correctness:       {evaluation.avg_correctness:.1f}/5")
    print(f"  Avg Completeness:      {evaluation.avg_completeness:.1f}/5")
    print(f"  Avg Faithfulness:      {evaluation.avg_faithfulness:.1f}/5")
    print(f"  Avg Retrieval Prec:    {evaluation.avg_retrieval_precision:.2f}")
    print(f"  Avg Retrieval Recall:  {evaluation.avg_retrieval_recall:.2f}")
    if evaluation.extra_aggregates:
        _print_extra_aggregates(evaluation.extra_aggregates)

    if evaluation.code_quality is not None:
        cq = evaluation.code_quality
        sm = cq.static_metrics
        print("\n  Code Quality (static):")
        print(f"    SLOC:                {sm.sloc}")
        print(f"    Avg CC:              {sm.avg_cyclomatic_complexity:.1f} ({sm.complexity_grade})")
        print(f"    Maintainability:     {sm.maintainability_index:.1f} ({sm.maintainability_grade})")
        print(f"    Halstead Bugs:       {sm.halstead_bugs:.2f}")
        print(f"    Framework Imports:   {sm.num_framework_imports}/{sm.num_imports}")
        print(f"    Type Annotations:    {sm.type_annotation_ratio:.0%}")
        if cq.code_review is not None:
            cr = cq.code_review
            print("  Code Quality (LLM review):")
            print(f"    Avg Score:           {cr.avg_score:.1f}/5")
            print(f"    Readability:         {cr.readability}/5")
            print(f"    Idiomatic Usage:     {cr.idiomatic_usage}/5")
            print(f"    Error Handling:      {cr.error_handling}/5")
            print(f"    Extensibility:       {cr.extensibility}/5")
            print(f"    Testability:         {cr.testability}/5")
            print(f"    Documentation:       {cr.documentation}/5")
            print(f"    Abstraction:         {cr.abstraction}/5")

    output_path = save_results(evaluation, RESULTS_DIR)
    print(f"  Results saved to:      {output_path}")

    return evaluation


FRAMEWORKS = ["pydantic_ai", "langgraph", "smolagents"]


async def main():
    parser = argparse.ArgumentParser(description="Run framework benchmark evaluation")
    parser.add_argument("--framework", choices=FRAMEWORKS, help="Framework to evaluate")
    parser.add_argument("--all", action="store_true", help="Evaluate all frameworks")
    parser.add_argument("--scenario", required=True, help="Scenario name (e.g., rag_qa)")
    parser.add_argument(
        "--mode",
        choices=["baseline", "capability"],
        default="baseline",
        help=(
            "Evaluation mode. baseline=fixed scenario pipeline, "
            "capability=scenario-specific framework extensions."
        ),
    )
    parser.add_argument("--judge-model", default="gpt-4o-mini", help="Model for LLM judge")
    parser.add_argument(
        "--skip-code-quality",
        action="store_true",
        help="Skip code quality evaluation entirely",
    )
    parser.add_argument(
        "--skip-code-review",
        action="store_true",
        help="Skip LLM code review (static analysis only)",
    )
    parser.add_argument(
        "--no-shared-store",
        action="store_true",
        help="Disable shared embedding store (each framework embeds independently)",
    )
    args = parser.parse_args()

    if not args.framework and not args.all:
        parser.error("Specify --framework or --all")

    scenario = load_scenario(args.scenario)

    embedding_store = None
    if not args.no_shared_store:
        print("Creating shared embedding store...")
        embedding_store = create_embedding_store(scenario)
        print(f"  Ingested {len(scenario.documents)} documents, store ready.")

    frameworks_to_run = FRAMEWORKS if args.all else [args.framework]
    evaluations: list[FrameworkEvaluation] = []

    for fw in frameworks_to_run:
        try:
            evaluation = await run_single(
                fw,
                scenario,
                args.mode,
                args.judge_model,
                skip_code_quality=args.skip_code_quality,
                skip_code_review=args.skip_code_review,
                embedding_store=embedding_store,
            )
            evaluations.append(evaluation)
        except Exception as e:
            print(f"\nError evaluating {fw}: {e}")
            import traceback

            traceback.print_exc()

    if evaluations:
        comparison_report = generate_comparison_report([dataclasses.asdict(e) for e in evaluations])
        comparison_path = RESULTS_DIR / f"comparison_{scenario.name}_{args.mode}.md"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        comparison_path.write_text(comparison_report)
        print(f"\nComparison report written to: {comparison_path}")

    if embedding_store is not None:
        embedding_store.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
