# Tooling Contract (Scenario Intent)

This scenario is designed for agentic workflows using tools.

Recommended minimal tool set:

- `run_sql(query: str)` for data retrieval and joins.
- `lookup_doc(name: str)` for policy lookups in markdown documents.

Expected behavior:

1. Start from the user question.
2. Gather facts from SQL.
3. Pull policy clauses only when needed.
4. Branch based on evidence (for example, escalation thresholds, exclusions, or tier-specific rules).
5. Return final answer with grounded sources.

The SQL seed is in `data/seed.sql`.
