---
name: add-scenario
description: >
  Scaffold a new evaluation scenario for the benchmark. Use when the user wants to add
  a new test scenario beyond RAG Q&A (e.g., multi-step reasoning, tool use, summarization).
  Creates the scenario directory with spec, documents, and questions files.
---

# Add Scenario

## When to use
Use when the user wants to add a new benchmark scenario.

## Steps

1. Create scenario directory:
   ```
   scenarios/<scenario_name>/
   ├── AGENTS.md
   ├── spec.yaml
   ├── documents/
   │   └── *.md
   └── questions.yaml
   ```

2. Create `spec.yaml`:
   ```yaml
   name: <scenario_name>
   version: "1.0"
   description: "<what this scenario tests>"
   documents_dir: documents/
   questions_file: questions.yaml
   config:
     embedding_model: text-embedding-3-small
     llm_model: gpt-5-mini
     chunk_size: 500
     chunk_overlap: 50
     top_k: 3
   ```

3. Create test documents in `documents/` — small markdown files (<500 words each)

4. Create `questions.yaml`:
   ```yaml
   scenario: <scenario_name>
   description: "<description>"
   questions:
     - id: q1
       text: "<question>"
       expected_answer: "<reference answer>"
       expected_sources:
         - <document_filename.md>
   ```

5. Write `AGENTS.md` describing the scenario

6. If the scenario requires a different interface than `RAGFramework`:
   - Extend `shared/src/shared/interface.py` with a new Protocol
   - Update the evaluation harness to support it
   - Each framework will need a new implementation file

## Important
- Keep documents small and self-contained
- Questions should have unambiguous expected answers
- Test with at least one framework before considering done
