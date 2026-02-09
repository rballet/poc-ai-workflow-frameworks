"""LLM-as-judge for implementation code quality review."""

from __future__ import annotations

import json
from dataclasses import dataclass

from openai import AsyncOpenAI

CODE_REVIEW_SYSTEM_PROMPT = """\
You are an expert Python code reviewer specialising in AI/ML framework code.

You will be given:
- A FRAMEWORK name (the AI agent framework being evaluated)
- A SCENARIO description (what the code is supposed to do)
- The full SOURCE CODE of the implementation

Score the code on seven criteria, each on a 1-5 scale:

1. READABILITY (1-5): How easy is the code to read and understand?
   Consider naming, formatting, logical flow, and cognitive load.
   1 = very confusing, 3 = adequate, 5 = immediately clear

2. IDIOMATIC USAGE (1-5): Does the code use the framework's APIs correctly
   and follow its recommended patterns?
   1 = fights the framework, 3 = basic usage, 5 = expert-level idiomatic code

3. ERROR HANDLING (1-5): How robustly does the code handle edge cases,
   exceptions, and invalid states?
   1 = no error handling, 3 = handles obvious cases, 5 = comprehensive

4. EXTENSIBILITY (1-5): How easy would it be to add new features
   (new retrieval strategies, different models, extra pipeline steps)?
   1 = requires rewrite, 3 = moderate refactoring, 5 = plug-and-play

5. TESTABILITY (1-5): How easy would it be to write unit tests?
   Are components isolated? Can dependencies be mocked?
   1 = monolithic/untestable, 3 = partially testable, 5 = fully testable

6. DOCUMENTATION (1-5): Quality of docstrings, comments, and
   self-documenting code.
   1 = no docs, 3 = some docstrings, 5 = thorough and helpful

7. ABSTRACTION (1-5): Appropriate level of abstraction—not over-engineered,
   not too monolithic.
   1 = wrong abstraction level, 3 = acceptable, 5 = just right

Respond in JSON:
{"readability": <int>, "idiomatic_usage": <int>, "error_handling": <int>, \
"extensibility": <int>, "testability": <int>, "documentation": <int>, \
"abstraction": <int>, "reasoning": "<brief explanation of scores>"}
"""


@dataclass
class CodeReviewScores:
    """Subjective code quality scores from LLM-as-judge."""

    readability: int
    idiomatic_usage: int
    error_handling: int
    extensibility: int
    testability: int
    documentation: int
    abstraction: int
    avg_score: float
    reasoning: str


async def review_code(
    source_code: str,
    framework_name: str,
    scenario_description: str,
    model: str = "gpt-4o-mini",
) -> CodeReviewScores:
    """Use an LLM to review implementation code quality."""
    client = AsyncOpenAI()
    user_prompt = (
        f"FRAMEWORK: {framework_name}\n\n"
        f"SCENARIO: {scenario_description}\n\n"
        f"SOURCE CODE:\n```python\n{source_code}\n```"
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CODE_REVIEW_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    data = json.loads(response.choices[0].message.content)

    scores = [
        data["readability"],
        data["idiomatic_usage"],
        data["error_handling"],
        data["extensibility"],
        data["testability"],
        data["documentation"],
        data["abstraction"],
    ]

    return CodeReviewScores(
        readability=data["readability"],
        idiomatic_usage=data["idiomatic_usage"],
        error_handling=data["error_handling"],
        extensibility=data["extensibility"],
        testability=data["testability"],
        documentation=data["documentation"],
        abstraction=data["abstraction"],
        avg_score=round(sum(scores) / len(scores), 2),
        reasoning=data["reasoning"],
    )
