"""CLI: compare benchmark results across frameworks and generate a report."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
import math
from pathlib import Path
from typing import Any


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


def _fmt(val, fmt: str) -> str:
    """Format a single value according to a format spec."""
    if fmt == "s":
        return str(val)
    if fmt == ",d":
        return f"{int(val):,}"
    if fmt.endswith("%"):
        return f"{val:{fmt}}"
    if "cost" in fmt:
        return f"${val:.4f}"
    return f"{val:{fmt}}"


def _label_from_key(key: str) -> str:
    """Convert snake_case metric names to readable labels."""
    return key.replace("_", " ").title()


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _percentile(values: list[float], p: float) -> float:
    """Linear-interpolated percentile with p in [0, 1]."""
    if not values:
        return 0.0
    if p <= 0:
        return min(values)
    if p >= 1:
        return max(values)
    sorted_vals = sorted(values)
    position = (len(sorted_vals) - 1) * p
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return sorted_vals[lower]
    weight = position - lower
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight


def _min_max_scale(
    value: float,
    series: list[float],
    *,
    higher_is_better: bool,
) -> float:
    low = min(series)
    high = max(series)
    if abs(high - low) < 1e-12:
        return 1.0
    if higher_is_better:
        return (value - low) / (high - low)
    return (high - value) / (high - low)


def _scenario_capability_signals(extra: dict[str, Any]) -> list[float]:
    """Return normalized scenario-specific quality signals, if present."""
    candidate_keys = [
        "branching_success_rate",
        "multi_hop_chain_success_rate",
        "branching_avg_grounded_hop_coverage",
        "multi_hop_avg_grounded_hop_coverage",
        "branching_avg_hop_coverage",
        "multi_hop_avg_hop_coverage",
    ]
    values: list[float] = []
    for key in candidate_keys:
        numeric = _numeric(extra.get(key))
        if numeric is None:
            continue
        values.append(max(0.0, min(1.0, numeric)))
    return values


def _build_scorecard(results: list[dict]) -> dict[str, dict[str, float | None]]:
    """Compute derived 0-100 scores from already-collected metrics."""
    latencies = [float(r.get("avg_latency", 0.0)) for r in results]
    costs = [float(r.get("total_cost_usd", 0.0)) for r in results]
    tokens = [float(r.get("total_tokens", 0.0)) for r in results]

    # Optional DX series
    mi_series: list[float] = []
    cc_series: list[float] = []
    review_series: list[float] = []
    for r in results:
        static = (r.get("code_quality") or {}).get("static_metrics") or {}
        mi = _numeric(static.get("maintainability_index"))
        cc = _numeric(static.get("avg_cyclomatic_complexity"))
        if mi is not None:
            mi_series.append(mi)
        if cc is not None:
            cc_series.append(cc)
        review = _numeric(((r.get("code_quality") or {}).get("code_review") or {}).get("avg_score"))
        if review is not None:
            review_series.append(review)

    scores: dict[str, dict[str, float | None]] = {}
    for r in results:
        name = str(r.get("framework_name", "unknown"))
        extra = r.get("extra_aggregates") or {}

        correctness = max(0.0, min(1.0, float(r.get("avg_correctness", 0.0)) / 5.0))
        completeness = max(0.0, min(1.0, float(r.get("avg_completeness", 0.0)) / 5.0))
        faithfulness = max(0.0, min(1.0, float(r.get("avg_faithfulness", 0.0)) / 5.0))
        base_capability = _mean([correctness, completeness, faithfulness])
        scenario_signals = _scenario_capability_signals(extra)
        capability = _mean([base_capability, *scenario_signals])

        latency_score = _min_max_scale(float(r.get("avg_latency", 0.0)), latencies, higher_is_better=False)
        cost_score = _min_max_scale(float(r.get("total_cost_usd", 0.0)), costs, higher_is_better=False)
        token_score = _min_max_scale(float(r.get("total_tokens", 0.0)), tokens, higher_is_better=False)
        efficiency = _mean([
            0.4 * latency_score,
            0.4 * cost_score,
            0.2 * token_score,
        ])

        static = (r.get("code_quality") or {}).get("static_metrics") or {}
        dx_parts: list[float] = []
        mi = _numeric(static.get("maintainability_index"))
        if mi is not None and mi_series:
            dx_parts.append(_min_max_scale(mi, mi_series, higher_is_better=True))
        cc = _numeric(static.get("avg_cyclomatic_complexity"))
        if cc is not None and cc_series:
            dx_parts.append(_min_max_scale(cc, cc_series, higher_is_better=False))
        type_ratio = _numeric(static.get("type_annotation_ratio"))
        if type_ratio is not None:
            dx_parts.append(max(0.0, min(1.0, type_ratio)))
        review = _numeric(((r.get("code_quality") or {}).get("code_review") or {}).get("avg_score"))
        if review is not None and review_series:
            dx_parts.append(max(0.0, min(1.0, review / 5.0)))
        dx = _mean(dx_parts) if dx_parts else None

        scores[name] = {
            "capability": 100.0 * capability,
            "efficiency": 100.0 * efficiency,
            "dx": (100.0 * dx) if dx is not None else None,
        }
    return scores


def _latency_percentiles(result: dict) -> tuple[float, float]:
    values = [
        float(q.get("latency_seconds", 0.0))
        for q in result.get("questions", [])
        if isinstance(q, dict)
    ]
    return _percentile(values, 0.50), _percentile(values, 0.95)


def generate_comparison_report(results: list[dict]) -> str:
    """Generate a markdown comparison report from multiple framework results."""
    lines: list[str] = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines.append("# Framework Comparison Report")
    lines.append("")
    lines.append(f"Generated: {timestamp}")
    if results:
        lines.append(f"Scenario: {results[0].get('scenario_name', 'unknown')}")
        lines.append(f"Scenario Type: {results[0].get('scenario_type', 'unknown')}")
        lines.append(f"Mode: {results[0].get('evaluation_mode', 'baseline')}")
        lines.append(f"Profile: {results[0].get('evaluation_profile', 'default')}")
        n_questions = len(results[0].get("questions", []))
        lines.append(f"Questions: {n_questions}")
    lines.append("")

    # --- Summary table ---
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

    # --- Derived scorecard ---
    lines.append("## Derived Scorecard (0-100)")
    lines.append("")
    lines.append(
        "These derived scores are computed from existing metrics and shown as "
        "decision aids (not as a single winner metric)."
    )
    lines.append("")
    scorecard = _build_scorecard(results)
    headers = ["Axis"] + [r["framework_name"] for r in results]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for axis, label in [
        ("capability", "Capability"),
        ("efficiency", "Efficiency"),
        ("dx", "Developer Experience"),
    ]:
        row = [label]
        for r in results:
            framework_name = r["framework_name"]
            value = scorecard.get(framework_name, {}).get(axis)
            if value is None:
                row.append("N/A")
            else:
                row.append(f"{value:.1f}")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # --- Stability proxies ---
    lines.append("## Runtime Distribution")
    lines.append("")
    headers = ["Metric"] + [r["framework_name"] for r in results]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    p50_row = ["Latency p50 (s)"]
    p95_row = ["Latency p95 (s)"]
    for r in results:
        p50, p95 = _latency_percentiles(r)
        p50_row.append(f"{p50:.2f}")
        p95_row.append(f"{p95:.2f}")
    lines.append("| " + " | ".join(p50_row) + " |")
    lines.append("| " + " | ".join(p95_row) + " |")
    lines.append("")

    # --- Extra aggregate metrics ---
    extra_keys: set[str] = set()
    for r in results:
        extra = r.get("extra_aggregates") or {}
        extra_keys.update(k for k, v in extra.items() if _numeric(v) is not None)

    if extra_keys:
        lines.append("## Scenario-Specific Metrics")
        lines.append("")
        headers = ["Metric"] + [r["framework_name"] for r in results]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for key in sorted(extra_keys):
            row = [_label_from_key(key)]
            for r in results:
                value = (r.get("extra_aggregates") or {}).get(key)
                numeric_value = _numeric(value)
                if numeric_value is None:
                    row.append("N/A")
                elif abs(numeric_value - int(numeric_value)) < 1e-9:
                    row.append(str(int(numeric_value)))
                else:
                    row.append(f"{numeric_value:.3f}")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    # --- Code Quality: Static Metrics ---
    has_code_quality = any(r.get("code_quality") for r in results)
    if has_code_quality:
        lines.append("## Code Quality — Static Metrics")
        lines.append("")

        headers = ["Metric"] + [r["framework_name"] for r in results]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        static_rows = [
            ("Source Lines (SLOC)", "sloc", "d"),
            ("Comment Ratio", "comment_ratio", ".0%"),
            ("Avg Cyclomatic Complexity", "avg_cyclomatic_complexity", ".1f"),
            ("Max Cyclomatic Complexity", "max_cyclomatic_complexity", "d"),
            ("Complexity Grade", "complexity_grade", "s"),
            ("Maintainability Index", "maintainability_index", ".1f"),
            ("Maintainability Grade", "maintainability_grade", "s"),
            ("Halstead Volume", "halstead_volume", ".0f"),
            ("Halstead Difficulty", "halstead_difficulty", ".1f"),
            ("Halstead Bugs (est.)", "halstead_bugs", ".2f"),
            ("Total Imports", "num_imports", "d"),
            ("Framework Imports", "num_framework_imports", "d"),
            ("Classes", "num_classes", "d"),
            ("Functions", "num_functions", "d"),
            ("Type Annotation Coverage", "type_annotation_ratio", ".0%"),
        ]

        for label, key, fmt in static_rows:
            row = [label]
            for r in results:
                cq = r.get("code_quality")
                sm = cq.get("static_metrics") if cq else None
                if sm and key in sm:
                    row.append(_fmt(sm[key], fmt))
                else:
                    row.append("N/A")
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")

        # --- Code Quality: LLM Code Review ---
        has_review = any(
            (r.get("code_quality") or {}).get("code_review") for r in results
        )
        if has_review:
            lines.append("## Code Quality — LLM Code Review")
            lines.append("")

            headers = ["Criterion"] + [r["framework_name"] for r in results]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

            review_rows = [
                ("Readability", "readability"),
                ("Idiomatic Usage", "idiomatic_usage"),
                ("Error Handling", "error_handling"),
                ("Extensibility", "extensibility"),
                ("Testability", "testability"),
                ("Documentation", "documentation"),
                ("Abstraction", "abstraction"),
                ("**Average**", "avg_score"),
            ]

            for label, key in review_rows:
                row = [label]
                for r in results:
                    cr = (r.get("code_quality") or {}).get("code_review")
                    if cr and key in cr:
                        val = cr[key]
                        fmt = ".1f" if key == "avg_score" else "d"
                        row.append(f"{val:{fmt}}")
                    else:
                        row.append("N/A")
                lines.append("| " + " | ".join(row) + " |")

            lines.append("")

    # --- Per-question breakdown ---
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

            extra_q_keys: set[str] = set()
            for r in results:
                r_questions = r.get("questions", [])
                if i < len(r_questions):
                    extra_metrics = r_questions[i].get("extra_metrics") or {}
                    extra_q_keys.update(k for k, v in extra_metrics.items() if _numeric(v) is not None)
            for key in sorted(extra_q_keys):
                q_metrics.append((_label_from_key(key), f"extra_metrics.{key}", ".3f"))

            for label, key, fmt in q_metrics:
                row = [label]
                for r in results:
                    r_questions = r.get("questions", [])
                    if i < len(r_questions):
                        if key.startswith("extra_metrics."):
                            extra_key = key.split(".", 1)[1]
                            val = (r_questions[i].get("extra_metrics") or {}).get(extra_key, None)
                        else:
                            val = r_questions[i].get(key, 0)
                        numeric_val = _numeric(val)
                        if numeric_val is None:
                            row.append("N/A")
                            continue
                        if fmt == ",d":
                            row.append(f"{int(numeric_val):,}")
                        elif fmt == ".3f" and abs(numeric_val - int(numeric_val)) < 1e-9:
                            row.append(str(int(numeric_val)))
                        else:
                            row.append(f"{numeric_val:{fmt}}")
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
