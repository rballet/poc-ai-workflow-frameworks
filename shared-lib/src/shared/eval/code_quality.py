"""Static code quality metrics via radon and ast analysis."""

from __future__ import annotations

import ast
from dataclasses import dataclass

from radon.complexity import cc_rank, cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze

# Mapping from framework key → import prefixes considered framework-specific.
_FRAMEWORK_IMPORT_PREFIXES: dict[str, list[str]] = {
    "langgraph": ["langgraph", "langchain", "langchain_openai", "langchain_core", "langchain_community"],
    "pydantic_ai": ["pydantic_ai"],
    "smolagents": ["smolagents", "litellm"],
}


@dataclass
class StaticMetrics:
    """Deterministic code metrics from radon and ast analysis."""

    # Size
    loc: int
    sloc: int
    comments: int
    blank: int
    comment_ratio: float
    # Complexity
    avg_cyclomatic_complexity: float
    max_cyclomatic_complexity: int
    complexity_grade: str  # A–F
    # Maintainability
    maintainability_index: float  # 0–100
    maintainability_grade: str  # A / B / C
    # Halstead
    halstead_volume: float
    halstead_difficulty: float
    halstead_effort: float
    halstead_bugs: float
    # Structure
    num_imports: int
    num_framework_imports: int
    num_classes: int
    num_functions: int
    type_annotation_ratio: float


def _mi_grade(score: float) -> str:
    """Map maintainability index to A/B/C grade."""
    if score >= 20:
        return "A"
    if score >= 10:
        return "B"
    return "C"


def _ast_metrics(source: str, framework_name: str) -> dict:
    """Walk the AST to count imports, classes, functions, and type annotations."""
    tree = ast.parse(source)

    prefixes = _FRAMEWORK_IMPORT_PREFIXES.get(framework_name.lower().replace(" ", "_"), [])

    num_imports = 0
    num_framework_imports = 0
    num_classes = 0
    num_functions = 0
    num_annotated_returns = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            num_imports += len(node.names)
            for alias in node.names:
                if any(alias.name == p or alias.name.startswith(p + ".") for p in prefixes):
                    num_framework_imports += 1

        elif isinstance(node, ast.ImportFrom):
            num_imports += 1
            module = node.module or ""
            if any(module == p or module.startswith(p + ".") for p in prefixes):
                num_framework_imports += 1

        elif isinstance(node, ast.ClassDef):
            num_classes += 1

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_functions += 1
            if node.returns is not None:
                num_annotated_returns += 1

    annotation_ratio = num_annotated_returns / num_functions if num_functions > 0 else 0.0

    return {
        "num_imports": num_imports,
        "num_framework_imports": num_framework_imports,
        "num_classes": num_classes,
        "num_functions": num_functions,
        "type_annotation_ratio": annotation_ratio,
    }


def compute_static_metrics(source: str, framework_name: str) -> StaticMetrics:
    """Compute deterministic static code metrics from Python source code.

    Parameters
    ----------
    source:
        The full Python source code as a string.
    framework_name:
        Framework key (e.g. ``"langgraph"``) used to identify
        framework-specific imports.
    """
    # --- Raw metrics (LOC, SLOC, comments, blank) ---
    raw = analyze(source)

    # --- Cyclomatic complexity ---
    cc_results = cc_visit(source)
    if cc_results:
        complexities = [block.complexity for block in cc_results]
        avg_cc = sum(complexities) / len(complexities)
        max_cc = max(complexities)
    else:
        avg_cc = 0.0
        max_cc = 0
    cc_grade = cc_rank(avg_cc) if cc_results else "A"

    # --- Maintainability index ---
    mi_score = mi_visit(source, multi=True)

    # --- Halstead ---
    h_results = h_visit(source)
    if h_results and hasattr(h_results, "total") and h_results.total:
        total = h_results.total
        h_volume = total.volume or 0.0
        h_difficulty = total.difficulty or 0.0
        h_effort = total.effort or 0.0
        h_bugs = total.bugs or 0.0
    elif h_results and isinstance(h_results, list) and len(h_results) > 0:
        # Aggregate across function-level results
        volumes = [h.volume for h in h_results if h.volume]
        difficulties = [h.difficulty for h in h_results if h.difficulty]
        efforts = [h.effort for h in h_results if h.effort]
        bugs = [h.bugs for h in h_results if h.bugs]
        h_volume = sum(volumes) if volumes else 0.0
        h_difficulty = (sum(difficulties) / len(difficulties)) if difficulties else 0.0
        h_effort = sum(efforts) if efforts else 0.0
        h_bugs = sum(bugs) if bugs else 0.0
    else:
        h_volume = 0.0
        h_difficulty = 0.0
        h_effort = 0.0
        h_bugs = 0.0

    # --- AST-based counts ---
    ast_counts = _ast_metrics(source, framework_name)

    return StaticMetrics(
        loc=raw.loc,
        sloc=raw.sloc,
        comments=raw.comments,
        blank=raw.blank,
        comment_ratio=raw.comments / raw.sloc if raw.sloc > 0 else 0.0,
        avg_cyclomatic_complexity=round(avg_cc, 2),
        max_cyclomatic_complexity=max_cc,
        complexity_grade=cc_grade,
        maintainability_index=round(mi_score, 2),
        maintainability_grade=_mi_grade(mi_score),
        halstead_volume=round(h_volume, 2),
        halstead_difficulty=round(h_difficulty, 2),
        halstead_effort=round(h_effort, 2),
        halstead_bugs=round(h_bugs, 4),
        num_imports=ast_counts["num_imports"],
        num_framework_imports=ast_counts["num_framework_imports"],
        num_classes=ast_counts["num_classes"],
        num_functions=ast_counts["num_functions"],
        type_annotation_ratio=round(ast_counts["type_annotation_ratio"], 2),
    )
