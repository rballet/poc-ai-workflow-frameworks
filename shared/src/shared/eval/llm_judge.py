"""LLM-as-judge for answer quality evaluation."""

from __future__ import annotations

import json
from dataclasses import dataclass

from openai import AsyncOpenAI

JUDGE_SYSTEM_PROMPT = """\
You are an expert evaluator for RAG (Retrieval-Augmented Generation) systems.

You will be given:
- A QUESTION the user asked
- An EXPECTED ANSWER (the ground truth reference)
- An ACTUAL ANSWER (produced by the system being evaluated)
- RETRIEVED SOURCES (document names the system used)

Score the ACTUAL ANSWER on three criteria, each on a 1-5 scale:

1. CORRECTNESS (1-5): Is the actual answer factually correct compared to the expected answer?
   1 = completely wrong, 3 = partially correct, 5 = fully correct

2. COMPLETENESS (1-5): Does the actual answer cover all key points in the expected answer?
   1 = misses everything, 3 = covers some points, 5 = covers all points

3. FAITHFULNESS (1-5): Is the actual answer grounded in the retrieved sources without hallucination?
   1 = entirely hallucinated, 3 = mix of grounded and hallucinated, 5 = fully grounded

Respond in JSON:
{"correctness": <int>, "completeness": <int>, "faithfulness": <int>, "reasoning": "<brief explanation>"}
"""


@dataclass
class JudgeResult:
    correctness: float
    completeness: float
    faithfulness: float
    reasoning: str


async def judge_answer(
    question: str,
    expected: str,
    actual: str,
    context_sources: list[str],
    model: str = "gpt-4o-mini",
) -> JudgeResult:
    """Use an LLM to judge answer quality."""
    client = AsyncOpenAI()
    user_prompt = (
        f"QUESTION: {question}\n\n"
        f"EXPECTED ANSWER: {expected}\n\n"
        f"ACTUAL ANSWER: {actual}\n\n"
        f"RETRIEVED SOURCES: {', '.join(context_sources) if context_sources else 'None'}"
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    data = json.loads(response.choices[0].message.content)
    return JudgeResult(
        correctness=data["correctness"],
        completeness=data["completeness"],
        faithfulness=data["faithfulness"],
        reasoning=data["reasoning"],
    )
