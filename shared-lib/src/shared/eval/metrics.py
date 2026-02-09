"""Cost estimation from token usage."""

# USD per 1K tokens — update as pricing changes
COST_PER_1K_TOKENS: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    "gpt-4o": {"prompt": 0.0025, "completion": 0.01},
    "gpt-4o-mini-2024-07-18": {"prompt": 0.00015, "completion": 0.0006},
    "claude-sonnet-4-20250514": {"prompt": 0.003, "completion": 0.015},
    "claude-haiku-3-5-20241022": {"prompt": 0.0008, "completion": 0.004},
}


def _normalize_model_name(model_name: str) -> str:
    """Strip provider prefixes (e.g. 'openai/gpt-4o-mini' → 'gpt-4o-mini').

    Frameworks like smolagents (via LiteLLM) report model names with a
    provider prefix.  We normalise so the cost lookup table works regardless
    of how the framework reports the model.
    """
    if "/" in model_name:
        return model_name.rsplit("/", 1)[-1]
    return model_name


def compute_cost(
    model_name: str, prompt_tokens: int, completion_tokens: int
) -> float:
    """Estimate USD cost for a single LLM call. Returns 0.0 for unknown models."""
    normalised = _normalize_model_name(model_name)
    rates = COST_PER_1K_TOKENS.get(normalised, {"prompt": 0.0, "completion": 0.0})
    return (prompt_tokens / 1000 * rates["prompt"]) + (
        completion_tokens / 1000 * rates["completion"]
    )
