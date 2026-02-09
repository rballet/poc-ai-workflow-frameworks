"""CLI entry point: run evaluation for one or all frameworks on a scenario."""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from shared.interface import Document, Question
from shared.eval.harness import FrameworkEvaluation, evaluate_framework

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


def get_framework(name: str):
    """Import and instantiate a framework by name."""
    if name == "pydantic_ai":
        from impl_pydantic_ai.rag_qa import PydanticAIRAG
        return PydanticAIRAG()
    elif name == "langgraph":
        from impl_langgraph.rag_qa import LangGraphRAG
        return LangGraphRAG()
    elif name == "smolagents":
        from impl_smolagents.rag_qa import SmolAgentsRAG
        return SmolAgentsRAG()
    else:
        print(f"Error: unknown framework '{name}'")
        sys.exit(1)


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


async def run_single(framework_name: str, scenario_name: str, judge_model: str) -> FrameworkEvaluation:
    """Run evaluation for a single framework."""
    documents, questions, spec = load_scenario(scenario_name)
    framework = get_framework(framework_name)
    print(f"\n{'='*60}")
    print(f"Evaluating: {framework.name}")
    print(f"Scenario: {scenario_name} ({len(questions)} questions)")
    print(f"{'='*60}")

    evaluation = await evaluate_framework(
        framework=framework,
        documents=documents,
        questions=questions,
        scenario_name=scenario_name,
        judge_model=judge_model,
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
    args = parser.parse_args()

    if not args.framework and not args.all:
        parser.error("Specify --framework or --all")

    frameworks_to_run = FRAMEWORKS if args.all else [args.framework]

    for fw in frameworks_to_run:
        try:
            await run_single(fw, args.scenario, args.judge_model)
        except Exception as e:
            print(f"\nError evaluating {fw}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
