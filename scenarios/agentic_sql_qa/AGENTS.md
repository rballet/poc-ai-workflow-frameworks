# Agentic SQL QA Scenario

This scenario targets tool-based agent workflows that combine:

- Structured retrieval via SQL
- Unstructured policy retrieval via markdown docs
- Branching decision logic based on intermediate evidence

## Assets

- `spec.yaml` — scenario config and baseline/capability budgets
- `questions.yaml` — mixed easy and branching questions
- `documents/` — policy and escalation rules
- `data/seed.sql` — local SQLite seed for deterministic tool tests

## Design Intent

- Easy questions test direct lookup behavior.
- Branching questions test evidence-driven decisions and conditional tool use.
- Metadata includes `required_hops` and `required_tools` for profile metrics.
