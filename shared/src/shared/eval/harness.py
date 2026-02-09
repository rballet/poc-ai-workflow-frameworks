"""Evaluation harness — runs any RAGFramework through a scenario."""

from __future__ import annotations

from dataclasses import dataclass, field

from shared.interface import Document, Question, RAGFramework, RunResult
from shared.eval.llm_judge import JudgeResult, judge_answer
from shared.eval.metrics import compute_cost
from shared.eval.retrieval import retrieval_precision, retrieval_recall


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


@dataclass
class FrameworkEvaluation:
    """Aggregate evaluation for one framework across all questions."""

    framework_name: str
    scenario_name: str
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


async def evaluate_framework(
    framework: RAGFramework,
    documents: list[Document],
    questions: list[Question],
    scenario_name: str,
    judge_model: str = "gpt-4o-mini",
) -> FrameworkEvaluation:
    """Run a full evaluation of one framework on one scenario."""
    # 1. Ingest documents (not part of per-question timing)
    await framework.ingest(documents)

    evaluation = FrameworkEvaluation(
        framework_name=framework.name,
        scenario_name=scenario_name,
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
            )
        )

    # 6. Aggregates
    _compute_aggregates(evaluation)

    # 7. Cleanup
    await framework.cleanup()

    return evaluation
