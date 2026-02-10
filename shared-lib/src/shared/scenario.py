"""Scenario loading and normalization for benchmark runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from shared.interface import Document, Question


@dataclass(frozen=True)
class ScenarioDefinition:
    """Loaded scenario data and normalized config."""

    name: str
    version: str
    description: str
    scenario_type: str
    documents: list[Document]
    questions: list[Question]
    config: dict[str, Any] = field(default_factory=dict)
    modes: dict[str, dict[str, Any]] = field(default_factory=dict)
    evaluation: dict[str, Any] = field(default_factory=dict)


def load_scenario(scenarios_dir: Path, scenario_name: str) -> ScenarioDefinition:
    """Load a scenario directory into a typed ScenarioDefinition."""
    scenario_dir = scenarios_dir / scenario_name
    if not scenario_dir.exists():
        raise FileNotFoundError(f"Scenario '{scenario_name}' not found at {scenario_dir}")

    spec = yaml.safe_load((scenario_dir / "spec.yaml").read_text())
    docs_dir = scenario_dir / spec["documents_dir"]
    q_path = scenario_dir / spec["questions_file"]
    q_data = yaml.safe_load(q_path.read_text())

    documents = [
        Document(content=doc_path.read_text(), source=doc_path.name)
        for doc_path in sorted(docs_dir.glob("*.md"))
    ]

    questions = [
        Question(
            id=q["id"],
            text=q["text"],
            expected_answer=q["expected_answer"],
            expected_sources=q.get("expected_sources", []),
            metadata=q.get("metadata", {}),
        )
        for q in q_data["questions"]
    ]

    scenario_type = (
        spec.get("scenario_type")
        or q_data.get("scenario_type")
        or "rag_qa"
    )

    return ScenarioDefinition(
        name=spec.get("name", scenario_name),
        version=str(spec.get("version", "1.0")),
        description=spec.get("description", scenario_name),
        scenario_type=scenario_type,
        documents=documents,
        questions=questions,
        config=spec.get("config", {}),
        modes=spec.get("modes", {}),
        evaluation=spec.get("evaluation", {}),
    )
