"""CLI entry point: run evaluation for one or all frameworks on a scenario."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
import yaml

load_dotenv()  # Load .env file from project root

from shared.interface import Document, Question
from shared.eval.harness import FrameworkEvaluation, evaluate_framework
from shared.retrieval import EmbeddingStore

from compare import generate_comparison_report

ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_DIR = ROOT / "scenarios"
RESULTS_DIR = ROOT / "results"


def load_scenario(scenario_name: str) -> tuple[list[Document], list[Question], dict]:
    """Load documents and questions from a scenario directory."""
    scenario_dir = SCENARIOS_DIR / scenario_name
    if not scenario_dir.exists():
        print(f"Error: scenario '{scenario_name}' not found at {scenario_dir}")
        sys.exit(1)

    # Load spec
    with open(scenario_dir / "spec.yaml") as f:
        spec = yaml.safe_load(f)

    # Load documents
    docs_dir = scenario_dir / spec["documents_dir"]
    documents = []
    for doc_path in sorted(docs_dir.glob("*.md")):
        documents.append(
            Document(content=doc_path.read_text(), source=doc_path.name)
        )

    # Load questions
    with open(scenario_dir / spec["questions_file"]) as f:
        q_data = yaml.safe_load(f)

    questions = [
        Question(
            id=q["id"],
            text=q["text"],
            expected_answer=q["expected_answer"],
            expected_sources=q.get("expected_sources", []),
        )
        for q in q_data["questions"]
    ]

    return documents, questions, spec


def create_embedding_store(spec: dict, documents: list[Document]) -> EmbeddingStore:
    """Create and populate a shared EmbeddingStore from scenario config."""
    config = spec.get("config", {})
    store = EmbeddingStore(
        embedding_model=config.get("embedding_model", "text-embedding-3-small"),
        chunk_size=config.get("chunk_size", 500),
        chunk_overlap=config.get("chunk_overlap", 50),
        top_k=config.get("top_k", 3),
    )
    store.ingest(documents)
    return store


def get_framework(name: str, embedding_store: EmbeddingStore | None = None):
    """Import and instantiate a framework by name."""
    if name == "pydantic_ai":
        from impl_pydantic_ai.rag_qa import PydanticAIRAG
        return PydanticAIRAG(embedding_store=embedding_store)
    elif name == "langgraph":
        from impl_langgraph.rag_qa import LangGraphRAG
        return LangGraphRAG(embedding_store=embedding_store)
    elif name == "smolagents":
        from impl_smolagents.rag_qa import SmolAgentsRAG
        return SmolAgentsRAG(embedding_store=embedding_store)
    else:
        print(f"Error: unknown framework '{name}'")
        sys.exit(1)


def get_framework_source(name: str, scenario: str) -> str | None:
    """Resolve the path to a framework's implementation source file."""
    source_path = ROOT / "frameworks" / name / "src" / f"impl_{name}" / f"{scenario}.py"
    if not source_path.exists():
        print(f"Warning: source file not found at {source_path}")
        return None
    return str(source_path)


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


async def run_single(
    framework_name: str,
    scenario_name: str,
    judge_model: str,
    skip_code_quality: bool = False,
    skip_code_review: bool = False,
    embedding_store: EmbeddingStore | None = None,
    documents: list[Document] | None = None,
    questions: list[Question] | None = None,
    spec: dict | None = None,
) -> FrameworkEvaluation:
    """Run evaluation for a single framework."""
    if documents is None or questions is None or spec is None:
        documents, questions, spec = load_scenario(scenario_name)

    framework = get_framework(framework_name, embedding_store=embedding_store)
    print(f"\n{'='*60}")
    print(f"Evaluating: {framework.name}")
    print(f"Scenario: {scenario_name} ({len(questions)} questions)")
    print(f"{'='*60}")

    # Resolve source path for code quality evaluation
    source_path = None
    if not skip_code_quality:
        source_path = get_framework_source(framework_name, scenario_name)

    scenario_desc = spec.get("description", scenario_name)

    evaluation = await evaluate_framework(
        framework=framework,
        documents=documents,
        questions=questions,
        scenario_name=scenario_name,
        judge_model=judge_model,
        source_path=source_path,
        framework_key=framework_name,
        scenario_description=scenario_desc,
        skip_code_review=skip_code_review,
    )

    # Print summary
    print(f"\nResults for {evaluation.framework_name}:")
    print(f"  Avg Latency:           {evaluation.avg_latency:.2f}s")
    print(f"  Total Tokens:          {evaluation.total_tokens}")
    print(f"  Total Cost:            ${evaluation.total_cost_usd:.4f}")
    print(f"  Avg Correctness:       {evaluation.avg_correctness:.1f}/5")
    print(f"  Avg Completeness:      {evaluation.avg_completeness:.1f}/5")
    print(f"  Avg Faithfulness:      {evaluation.avg_faithfulness:.1f}/5")
    print(f"  Avg Retrieval Prec:    {evaluation.avg_retrieval_precision:.2f}")
    print(f"  Avg Retrieval Recall:  {evaluation.avg_retrieval_recall:.2f}")

    # Code quality summary
    if evaluation.code_quality is not None:
        cq = evaluation.code_quality
        sm = cq.static_metrics
        print(f"\n  Code Quality (static):")
        print(f"    SLOC:                {sm.sloc}")
        print(f"    Avg CC:              {sm.avg_cyclomatic_complexity:.1f} ({sm.complexity_grade})")
        print(f"    Maintainability:     {sm.maintainability_index:.1f} ({sm.maintainability_grade})")
        print(f"    Halstead Bugs:       {sm.halstead_bugs:.2f}")
        print(f"    Framework Imports:   {sm.num_framework_imports}/{sm.num_imports}")
        print(f"    Type Annotations:    {sm.type_annotation_ratio:.0%}")
        if cq.code_review is not None:
            cr = cq.code_review
            print(f"  Code Quality (LLM review):")
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
    parser.add_argument("--judge-model", default="gpt-4o-mini", help="Model for LLM judge")
    parser.add_argument(
        "--skip-code-quality", action="store_true",
        help="Skip code quality evaluation entirely",
    )
    parser.add_argument(
        "--skip-code-review", action="store_true",
        help="Skip LLM code review (static analysis only)",
    )
    parser.add_argument(
        "--no-shared-store", action="store_true",
        help="Disable shared embedding store (each framework embeds independently)",
    )
    args = parser.parse_args()

    if not args.framework and not args.all:
        parser.error("Specify --framework or --all")

    # Load scenario once
    documents, questions, spec = load_scenario(args.scenario)

    # Create shared embedding store unless disabled
    embedding_store = None
    if not args.no_shared_store:
        print("Creating shared embedding store...")
        embedding_store = create_embedding_store(spec, documents)
        print(f"  Ingested {len(documents)} documents, store ready.")

    frameworks_to_run = FRAMEWORKS if args.all else [args.framework]
    evaluations: list[FrameworkEvaluation] = []

    for fw in frameworks_to_run:
        try:
            evaluation = await run_single(
                fw,
                args.scenario,
                args.judge_model,
                skip_code_quality=args.skip_code_quality,
                skip_code_review=args.skip_code_review,
                embedding_store=embedding_store,
                documents=documents,
                questions=questions,
                spec=spec,
            )
            evaluations.append(evaluation)
        except Exception as e:
            print(f"\nError evaluating {fw}: {e}")
            import traceback
            traceback.print_exc()

    # Generate comparison markdown from collected results
    if evaluations:
        comparison_report = generate_comparison_report(
            [dataclasses.asdict(e) for e in evaluations]
        )
        comparison_path = RESULTS_DIR / f"comparison_{args.scenario}.md"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        comparison_path.write_text(comparison_report)
        print(f"\nComparison report written to: {comparison_path}")

    # Cleanup shared store
    if embedding_store is not None:
        embedding_store.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
