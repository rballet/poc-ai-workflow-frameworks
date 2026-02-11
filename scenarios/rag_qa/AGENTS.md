# RAG Q&A Scenario

Simple Retrieval-Augmented Generation question answering over small technical documents.

## Documents
- `python_concurrency.md` — Threading, multiprocessing, asyncio, GIL
- `http_status_codes.md` — HTTP status code categories and specific codes
- `git_branching.md` — Branching strategies, merge vs rebase, GitHub Flow

## Questions
7 questions spanning all 3 documents. Each question targets one specific document. See `questions.yaml` for full list with expected answers.

## Configuration (spec.yaml)
- Embedding: `text-embedding-3-small`
- LLM: `gpt-5-mini`
- Chunk size: 500 chars, 50 overlap
- Top-K retrieval: 3 chunks
