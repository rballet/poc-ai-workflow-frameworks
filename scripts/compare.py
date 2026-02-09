"""CLI: compare benchmark results across frameworks and generate a report."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_results(paths: list[str]) -> list[dict]:
    """Load result JSON files."""
    results = []
    for path in paths:
        p = Path(path)
        if not p.exists():
            print(f"Warning: {path} not found, skipping")
            continue
        with open(p) as f:
            results.append(json.load(f))
    return results


def generate_comparison_report(results: list[dict]) -> str:
    """Generate a markdown comparison report from multiple framework results."""
    lines = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines.append("# Framework Comparison Report")
    lines.append("")
    lines.append(f"Generated: {timestamp}")
    if results:
        lines.append(f"Scenario: {results[0].get('scenario_name', 'unknown')}")
        n_questions = len(results[0].get("questions", []))
        lines.append(f"Questions: {n_questions}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")

    headers = ["Metric"] + [r["framework_name"] for r in results]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    metrics = [
        ("Avg Latency (s)", "avg_latency", ".2f"),
        ("Total Tokens", "total_tokens", ",d"),
        ("Est. Cost (USD)", "total_cost_usd", ".4f"),
        ("Avg Correctness (1-5)", "avg_correctness", ".1f"),
        ("Avg Completeness (1-5)", "avg_completeness", ".1f"),
        ("Avg Faithfulness (1-5)", "avg_faithfulness", ".1f"),
        ("Avg Retrieval Precision", "avg_retrieval_precision", ".2f"),
        ("Avg Retrieval Recall", "avg_retrieval_recall", ".2f"),
    ]

    for label, key, fmt in metrics:
        row = [label]
        for r in results:
            val = r.get(key, 0)
            if fmt == ",d":
                row.append(f"{int(val):,}")
            elif fmt == ".4f" and "cost" in key.lower():
                row.append(f"${val:{fmt}}")
            else:
                row.append(f"{val:{fmt}}")
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")

    # Per-question breakdown
    lines.append("## Per-Question Results")
    lines.append("")

    if results:
        questions = results[0].get("questions", [])
        for i, q in enumerate(questions):
            q_id = q.get("question_id", f"q{i+1}")
            q_text = q.get("question_text", "")
            lines.append(f"### {q_id}: {q_text}")
            lines.append("")

            headers = ["Metric"] + [r["framework_name"] for r in results]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

            q_metrics = [
                ("Latency (s)", "latency_seconds", ".2f"),
                ("Tokens", "total_tokens", ",d"),
                ("Correctness", "correctness_score", ".0f"),
                ("Completeness", "completeness_score", ".0f"),
                ("Faithfulness", "faithfulness_score", ".0f"),
                ("Retrieval Prec", "retrieval_precision", ".2f"),
                ("Retrieval Recall", "retrieval_recall", ".2f"),
            ]

            for label, key, fmt in q_metrics:
                row = [label]
                for r in results:
                    r_questions = r.get("questions", [])
                    if i < len(r_questions):
                        val = r_questions[i].get(key, 0)
                        if fmt == ",d":
                            row.append(f"{int(val):,}")
                        else:
                            row.append(f"{val:{fmt}}")
                    else:
                        row.append("N/A")
                lines.append("| " + " | ".join(row) + " |")

            lines.append("")

            # Show actual answers
            lines.append("**Answers:**")
            lines.append("")
            for r in results:
                r_questions = r.get("questions", [])
                if i < len(r_questions):
                    answer = r_questions[i].get("actual_answer", "N/A")
                    # Truncate long answers
                    if len(answer) > 300:
                        answer = answer[:300] + "..."
                    lines.append(f"- **{r['framework_name']}**: {answer}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare framework benchmark results")
    parser.add_argument("files", nargs="+", help="Result JSON files to compare")
    parser.add_argument(
        "-o", "--output", default=None, help="Output markdown file (default: stdout)"
    )
    args = parser.parse_args()

    results = load_results(args.files)
    if not results:
        print("Error: no valid result files found")
        sys.exit(1)

    report = generate_comparison_report(results)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        print(f"Report written to {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
