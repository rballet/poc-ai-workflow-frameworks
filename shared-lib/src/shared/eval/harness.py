"""Evaluation harness — runs any RAGFramework through a scenario."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from shared.interface import Document, Question, RAGFramework, RunResult
from shared.eval.llm_judge import JudgeResult, judge_answer
from shared.eval.metrics import compute_cost
from shared.eval.retrieval import retrieval_precision, retrieval_recall
from shared.eval.code_quality import StaticMetrics, compute_static_metrics
from shared.eval.code_review import CodeReviewScores, review_code
from shared.eval.profiles import ProfileContext, ScenarioProfile


@dataclass
class QuestionEvaluation:
    """Full evaluation of one question."""

    question_id: str
    question_text: str
    expected_answer: str
    actual_answer: str
    sources_expected: list[str]
    sources_retrieved: list[str]
    # Performance
    latency_seconds: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    model_name: str
    # Quality (1-5 from LLM judge)
    correctness_score: float
    completeness_score: float
    faithfulness_score: float
    judge_reasoning: str
    # Retrieval (0-1)
    retrieval_precision: float
    retrieval_recall: float
    # Scenario/profile specific metrics
    extra_metrics: dict[str, float | int | bool] = field(default_factory=dict)


@dataclass
class CodeQualityEvaluation:
    """Combined code quality assessment for a framework implementation."""

    source_file: str
    source_sloc: int
    static_metrics: StaticMetrics
    code_review: CodeReviewScores | None = None


@dataclass
class FrameworkEvaluation:
    """Aggregate evaluation for one framework across all questions."""

    framework_name: str
    scenario_name: str
    scenario_type: str = "rag_qa"
    evaluation_mode: str = "baseline"
    evaluation_profile: str = "default"
    questions: list[QuestionEvaluation] = field(default_factory=list)
    # Aggregates
    avg_latency: float = 0.0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_correctness: float = 0.0
    avg_completeness: float = 0.0
    avg_faithfulness: float = 0.0
    avg_retrieval_precision: float = 0.0
    avg_retrieval_recall: float = 0.0
    extra_aggregates: dict[str, float] = field(default_factory=dict)
    # Code quality (per-framework, not per-question)
    code_quality: CodeQualityEvaluation | None = None


def _compute_extra_aggregates(
    question_metrics: list[dict[str, float | int | bool]]
) -> dict[str, float]:
    """Compute mean value for all numeric per-question extra metrics."""
    numeric: dict[str, list[float]] = {}
    for metrics in question_metrics:
        for key, value in metrics.items():
            if isinstance(value, bool):
                numeric.setdefault(key, []).append(float(value))
            elif isinstance(value, (int, float)):
                numeric.setdefault(key, []).append(float(value))
    return {f"{k}_avg": sum(v) / len(v) for k, v in numeric.items() if v}


def _compute_aggregates(evaluation: FrameworkEvaluation) -> None:
    """Fill in aggregate fields from per-question data."""
    n = len(evaluation.questions)
    if n == 0:
        return
    evaluation.avg_latency = sum(q.latency_seconds for q in evaluation.questions) / n
    evaluation.total_tokens = sum(q.total_tokens for q in evaluation.questions)
    evaluation.total_cost_usd = sum(q.estimated_cost_usd for q in evaluation.questions)
    evaluation.avg_correctness = sum(q.correctness_score for q in evaluation.questions) / n
    evaluation.avg_completeness = sum(q.completeness_score for q in evaluation.questions) / n
    evaluation.avg_faithfulness = sum(q.faithfulness_score for q in evaluation.questions) / n
    evaluation.avg_retrieval_precision = sum(q.retrieval_precision for q in evaluation.questions) / n
    evaluation.avg_retrieval_recall = sum(q.retrieval_recall for q in evaluation.questions) / n
    evaluation.extra_aggregates = _compute_extra_aggregates(
        [q.extra_metrics for q in evaluation.questions]
    )


async def evaluate_framework(
    framework: RAGFramework,
    documents: list[Document],
    questions: list[Question],
    scenario_name: str,
    scenario_type: str = "rag_qa",
    evaluation_mode: str = "baseline",
    judge_model: str = "gpt-4o-mini",
    scenario_profile: ScenarioProfile | None = None,
    profile_context: ProfileContext | None = None,
    source_path: str | None = None,
    framework_key: str | None = None,
    scenario_description: str = "",
    skip_code_review: bool = False,
) -> FrameworkEvaluation:
    """Run a full evaluation of one framework on one scenario.

    Parameters
    ----------
    source_path:
        Path to the framework's implementation source file.  When provided,
        static analysis and (optionally) LLM code review are run.
    framework_key:
        Short identifier like ``"langgraph"`` used to classify imports.
    scenario_description:
        Human-readable description passed to the LLM code reviewer.
    skip_code_review:
        If *True*, skip the LLM code review (static analysis only).
    """
    # 1. Ingest documents (not part of per-question timing)
    await framework.ingest(documents)

    if scenario_profile is None:
        raise ValueError("scenario_profile must be provided")
    if profile_context is None:
        raise ValueError("profile_context must be provided")

    evaluation = FrameworkEvaluation(
        framework_name=framework.name,
        scenario_name=scenario_name,
        scenario_type=scenario_type,
        evaluation_mode=evaluation_mode,
        evaluation_profile=profile_context.profile_key,
    )

    for question in questions:
        # 2. Query
        result: RunResult = await framework.query(question.text)

        # 3. Cost
        cost = compute_cost(
            result.usage.model_name,
            result.usage.prompt_tokens,
            result.usage.completion_tokens,
        )

        # 4. LLM-as-judge
        judge: JudgeResult = await judge_answer(
            question=question.text,
            expected=question.expected_answer,
            actual=result.answer.text,
            context_sources=result.answer.sources_used,
            model=judge_model,
        )

        # 5. Retrieval metrics
        r_precision = retrieval_precision(
            retrieved=result.answer.sources_used,
            relevant=question.expected_sources,
        )
        r_recall = retrieval_recall(
            retrieved=result.answer.sources_used,
            relevant=question.expected_sources,
        )
        question_extra = scenario_profile.question_metrics(
            question=question,
            result=result,
            context=profile_context,
        )

        evaluation.questions.append(
            QuestionEvaluation(
                question_id=question.id,
                question_text=question.text,
                expected_answer=question.expected_answer,
                actual_answer=result.answer.text,
                sources_expected=question.expected_sources,
                sources_retrieved=result.answer.sources_used,
                latency_seconds=result.usage.latency_seconds,
                prompt_tokens=result.usage.prompt_tokens,
                completion_tokens=result.usage.completion_tokens,
                total_tokens=result.usage.total_tokens,
                estimated_cost_usd=cost,
                model_name=result.usage.model_name,
                correctness_score=judge.correctness,
                completeness_score=judge.completeness,
                faithfulness_score=judge.faithfulness,
                judge_reasoning=judge.reasoning,
                retrieval_precision=r_precision,
                retrieval_recall=r_recall,
                extra_metrics=question_extra,
            )
        )

    # 6. Aggregates
    _compute_aggregates(evaluation)
    evaluation.extra_aggregates.update(
        scenario_profile.aggregate_metrics(
            question_metrics=[q.extra_metrics for q in evaluation.questions],
            context=profile_context,
        )
    )

    # 7. Code quality (per-framework, not per-question)
    if source_path is not None:
        source_code = Path(source_path).read_text()
        static = compute_static_metrics(
            source_code, framework_key or framework.name
        )

        code_review_result = None
        if not skip_code_review:
            code_review_result = await review_code(
                source_code=source_code,
                framework_name=framework.name,
                scenario_description=scenario_description,
                model=judge_model,
            )

        evaluation.code_quality = CodeQualityEvaluation(
            source_file=source_path,
            source_sloc=static.sloc,
            static_metrics=static,
            code_review=code_review_result,
        )

    # 8. Cleanup
    await framework.cleanup()

    return evaluation
