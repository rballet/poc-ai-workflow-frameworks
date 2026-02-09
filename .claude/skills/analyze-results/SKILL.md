---
name: analyze-results
description: >
  Analyze and compare benchmark results across frameworks. Use when the user wants to
  interpret results, generate comparison tables, or understand which framework performed
  better and why. Reads JSON result files and generates human-readable analysis.
---

# Analyze Results

## When to use
Use when the user asks to analyze, compare, or interpret benchmark results.

## Steps

1. List available results:
   ```bash
   ls -la results/*.json
   ```

2. Generate comparison report:
   ```bash
   uv run python scripts/compare.py results/*.json -o results/comparison.md
   ```

3. Read the generated report:
   ```bash
   cat results/comparison.md
   ```

4. For deeper analysis, read individual JSON files:
   ```bash
   cat results/<framework>_<scenario>_<timestamp>.json
   ```

## Key Metrics to Compare

| Metric | What it tells you |
|--------|-------------------|
| Avg Latency | End-to-end response time including retrieval |
| Total Tokens | Overall token consumption (cost driver) |
| Est. Cost | USD estimate based on model pricing |
| Correctness (1-5) | Is the answer factually right? |
| Completeness (1-5) | Does it cover all key points? |
| Faithfulness (1-5) | Is it grounded in retrieved sources? |
| Retrieval Precision | Were the right documents retrieved? |
| Retrieval Recall | Were all relevant documents found? |

## Analysis Guidelines
- Look for significant differences (>0.5 points on quality scores)
- Note token efficiency (similar quality with fewer tokens = better)
- Consider latency vs quality tradeoffs
- Check retrieval metrics — poor retrieval indicates a framework issue, not LLM quality
- Compare per-question results to identify framework-specific strengths/weaknesses
