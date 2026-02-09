# Scenarios

Each subdirectory defines one benchmark scenario with:
- `spec.yaml` — Scenario configuration (model, chunk size, top_k)
- `documents/` — Small test documents (markdown, <500 words each)
- `questions.yaml` — Test questions with expected answers and expected sources

## Rules
- Documents MUST be small and self-contained.
- Questions MUST have clear expected answers and identify expected source documents.
- Scenarios are framework-agnostic — they define WHAT to test, not HOW.
- Add new scenarios as subdirectories following the same structure.
