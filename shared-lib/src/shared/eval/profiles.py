"""Scenario-specific evaluation profile extensions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from shared.interface import Question, RunResult

ScalarMetric = float | int | bool


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _dedupe_keep_order(items: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


@dataclass(frozen=True)
class ProfileContext:
    """Run context provided to scenario profiles."""

    scenario_name: str
    scenario_type: str
    mode: str
    profile_key: str
    profile_config: dict[str, Any]


class ScenarioProfile(ABC):
    """Pluggable extension point for scenario-specific quality metrics."""

    key: str = "default"

    @abstractmethod
    def question_metrics(
        self, question: Question, result: RunResult, context: ProfileContext
    ) -> dict[str, ScalarMetric]:
        """Return additional per-question metrics."""

    def aggregate_metrics(
        self, question_metrics: list[dict[str, ScalarMetric]], context: ProfileContext
    ) -> dict[str, float]:
        """Return additional aggregate metrics from per-question metrics."""
        numeric: dict[str, list[float]] = {}
        for metrics in question_metrics:
            for key, value in metrics.items():
                if isinstance(value, bool):
                    numeric.setdefault(key, []).append(float(value))
                elif isinstance(value, (int, float)):
                    numeric.setdefault(key, []).append(float(value))
        return {f"{k}_avg": _mean(v) for k, v in numeric.items()}


class DefaultScenarioProfile(ScenarioProfile):
    """No-op profile used for standard scenarios."""

    key = "default"

    def question_metrics(
        self, question: Question, result: RunResult, context: ProfileContext
    ) -> dict[str, ScalarMetric]:
        _ = (question, result, context)
        return {}


class MultiHopChainProfile(ScenarioProfile):
    """Metrics for multi-hop QA where each hop can be explicitly annotated."""

    key = "multihop_chain_qa"

    def question_metrics(
        self, question: Question, result: RunResult, context: ProfileContext
    ) -> dict[str, ScalarMetric]:
        _ = context
        metadata = question.metadata or {}
        hops = metadata.get("required_hops", [])
        is_multi_hop = bool(metadata.get("multi_hop", False) or len(hops) > 1)

        if not hops:
            return {"is_multi_hop": is_multi_hop}

        answer_text = _normalize_text(result.answer.text)
        retrieved_sources = set(result.answer.sources_used)

        matched_hops = 0
        sourced_hops = 0
        for hop in hops:
            aliases = [_normalize_text(a) for a in hop.get("any_of", []) if a]
            source = hop.get("source")

            hop_match = any(alias in answer_text for alias in aliases) if aliases else False
            if hop_match:
                matched_hops += 1
                if source and source in retrieved_sources:
                    sourced_hops += 1

        hop_count = len(hops)
        hop_coverage = _safe_ratio(matched_hops, hop_count)
        grounded_hop_coverage = _safe_ratio(sourced_hops, hop_count)

        return {
            "is_multi_hop": is_multi_hop,
            "required_hops": hop_count,
            "matched_hops": matched_hops,
            "hop_coverage": hop_coverage,
            "grounded_hop_coverage": grounded_hop_coverage,
            "chain_success": hop_coverage >= 1.0,
        }

    def aggregate_metrics(
        self, question_metrics: list[dict[str, ScalarMetric]], context: ProfileContext
    ) -> dict[str, float]:
        _ = context
        multi = [m for m in question_metrics if bool(m.get("is_multi_hop", False))]
        all_hop = [m for m in question_metrics if "hop_coverage" in m]

        result: dict[str, float] = {
            "multi_hop_questions": float(len(multi)),
            "annotated_hop_questions": float(len(all_hop)),
        }

        if multi:
            cov = [float(m["hop_coverage"]) for m in multi if "hop_coverage" in m]
            grounded = [
                float(m["grounded_hop_coverage"])
                for m in multi
                if "grounded_hop_coverage" in m
            ]
            chain_success = [
                1.0 if bool(m["chain_success"]) else 0.0
                for m in multi
                if "chain_success" in m
            ]
            if cov:
                result["multi_hop_avg_hop_coverage"] = _mean(cov)
            if grounded:
                result["multi_hop_avg_grounded_hop_coverage"] = _mean(grounded)
            if chain_success:
                result["multi_hop_chain_success_rate"] = _mean(chain_success)

        return result


class ToolBranchingProfile(ScenarioProfile):
    """Metrics for tool-oriented QA with easy and branching paths."""

    key = "tool_branching_qa"

    @staticmethod
    def _extract_tool_names(answer_metadata: dict[str, Any]) -> list[str]:
        names: list[str] = []
        traces = (
            answer_metadata.get("tool_trace")
            or answer_metadata.get("tools_used")
            or answer_metadata.get("tool_calls")
            or []
        )
        if not isinstance(traces, list):
            return []
        for item in traces:
            if isinstance(item, str):
                cleaned = item.strip()
                if cleaned:
                    names.append(cleaned)
                continue
            if isinstance(item, dict):
                candidate = item.get("tool") or item.get("name")
                if candidate:
                    names.append(str(candidate).strip())
        return _dedupe_keep_order([n for n in names if n])

    def question_metrics(
        self, question: Question, result: RunResult, context: ProfileContext
    ) -> dict[str, ScalarMetric]:
        _ = context
        qmeta = question.metadata or {}
        ameta = result.answer.metadata if isinstance(result.answer.metadata, dict) else {}

        hops = qmeta.get("required_hops", [])
        is_branching = bool(
            qmeta.get("branching", False)
            or int(qmeta.get("branching_points", 0)) > 0
            or len(hops) > 1
        )

        answer_text = _normalize_text(result.answer.text)
        retrieved_sources = set(result.answer.sources_used)

        matched_hops = 0
        grounded_hops = 0
        for hop in hops:
            aliases = [_normalize_text(a) for a in hop.get("any_of", []) if a]
            source = hop.get("source")
            if aliases and any(alias in answer_text for alias in aliases):
                matched_hops += 1
                if source and source in retrieved_sources:
                    grounded_hops += 1

        hop_count = len(hops)
        hop_coverage = _safe_ratio(matched_hops, hop_count) if hop_count else 0.0
        grounded_hop_coverage = (
            _safe_ratio(grounded_hops, hop_count) if hop_count else 0.0
        )

        expected_tools = [
            str(tool).strip()
            for tool in qmeta.get("required_tools", [])
            if str(tool).strip()
        ]
        expected_tools = _dedupe_keep_order(expected_tools)
        actual_tools = self._extract_tool_names(ameta)
        actual_lower = {tool.lower() for tool in actual_tools}
        matched_tools = sum(1 for tool in expected_tools if tool.lower() in actual_lower)
        tool_coverage = (
            _safe_ratio(matched_tools, len(expected_tools)) if expected_tools else 0.0
        )

        return {
            "is_branching": is_branching,
            "is_easy": not is_branching,
            "required_hops": hop_count,
            "matched_hops": matched_hops,
            "hop_coverage": hop_coverage,
            "grounded_hop_coverage": grounded_hop_coverage,
            "branching_success": (hop_coverage >= 1.0) if is_branching and hop_count else False,
            "required_tools": len(expected_tools),
            "matched_tools": matched_tools,
            "tool_coverage": tool_coverage,
            "has_tool_trace": bool(actual_tools),
            "tool_calls_reported": int(
                ameta.get("tool_calls", len(actual_tools))
            )
            if isinstance(ameta.get("tool_calls", len(actual_tools)), int)
            else len(actual_tools),
        }

    def aggregate_metrics(
        self, question_metrics: list[dict[str, ScalarMetric]], context: ProfileContext
    ) -> dict[str, float]:
        _ = context
        branching = [m for m in question_metrics if bool(m.get("is_branching", False))]
        easy = [m for m in question_metrics if bool(m.get("is_easy", False))]

        result: dict[str, float] = {
            "branching_questions": float(len(branching)),
            "easy_questions": float(len(easy)),
        }

        if branching:
            b_cov = [float(m["hop_coverage"]) for m in branching if "hop_coverage" in m]
            b_grounded = [
                float(m["grounded_hop_coverage"])
                for m in branching
                if "grounded_hop_coverage" in m
            ]
            b_success = [
                1.0 if bool(m.get("branching_success", False)) else 0.0
                for m in branching
            ]
            b_tool_cov = [
                float(m["tool_coverage"])
                for m in branching
                if float(m.get("required_tools", 0.0)) > 0.0
            ]
            if b_cov:
                result["branching_avg_hop_coverage"] = _mean(b_cov)
            if b_grounded:
                result["branching_avg_grounded_hop_coverage"] = _mean(b_grounded)
            if b_success:
                result["branching_success_rate"] = _mean(b_success)
            if b_tool_cov:
                result["branching_avg_tool_coverage"] = _mean(b_tool_cov)

        if easy:
            e_cov = [float(m["hop_coverage"]) for m in easy if "hop_coverage" in m]
            if e_cov:
                result["easy_avg_hop_coverage"] = _mean(e_cov)

        tool_trace = [
            1.0 if bool(m.get("has_tool_trace", False)) else 0.0
            for m in question_metrics
        ]
        if tool_trace:
            result["tool_trace_rate"] = _mean(tool_trace)

        return result


_PROFILE_REGISTRY: dict[str, ScenarioProfile] = {
    DefaultScenarioProfile.key: DefaultScenarioProfile(),
    MultiHopChainProfile.key: MultiHopChainProfile(),
    ToolBranchingProfile.key: ToolBranchingProfile(),
}


def get_scenario_profile(profile_key: str | None) -> ScenarioProfile:
    """Return a registered scenario profile (falls back to default)."""
    if not profile_key:
        return _PROFILE_REGISTRY[DefaultScenarioProfile.key]
    return _PROFILE_REGISTRY.get(profile_key, _PROFILE_REGISTRY[DefaultScenarioProfile.key])
