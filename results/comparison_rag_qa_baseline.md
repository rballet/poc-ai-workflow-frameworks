# Framework Comparison Report

Generated: 2026-02-12 22:10 UTC
Scenario: rag_qa
Scenario Type: rag_qa
Mode: baseline
Profile: default
Questions: 7

## Summary

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Avg Latency (s) | 6.42 | 5.89 | 5.79 | 10.27 |
| Total Tokens | 6,577 | 6,539 | 6,549 | 46,339 |
| Est. Cost (USD) | $0.0082 | $0.0082 | $0.0082 | $0.0655 |
| Avg Correctness (1-5) | 4.4 | 4.4 | 4.4 | 4.4 |
| Avg Completeness (1-5) | 4.3 | 4.3 | 4.1 | 4.3 |
| Avg Faithfulness (1-5) | 5.0 | 5.0 | 5.0 | 5.0 |
| Avg Retrieval Precision | 1.00 | 1.00 | 1.00 | 1.00 |
| Avg Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

## Derived Scorecard (0-100)

These derived scores are computed from existing metrics and shown as decision aids (not as a single winner metric).

| Axis | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Capability | 91.4 | 91.4 | 90.5 | 91.4 |
| Efficiency | 31.4 | 33.0 | 33.3 | 0.0 |
| Developer Experience | 72.2 | 64.0 | 67.9 | 65.2 |

## Runtime Distribution

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency p50 (s) | 5.76 | 5.49 | 5.64 | 10.44 |
| Latency p95 (s) | 8.98 | 7.71 | 8.74 | 12.40 |

## Code Quality — Static Metrics

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Source Lines (SLOC) | 147 | 205 | 165 | 163 |
| Comment Ratio | 2% | 1% | 2% | 2% |
| Avg Cyclomatic Complexity | 3.0 | 2.5 | 3.0 | 3.1 |
| Max Cyclomatic Complexity | 6 | 6 | 6 | 6 |
| Complexity Grade | A | A | A | A |
| Maintainability Index | 51.1 | 42.1 | 49.9 | 50.7 |
| Maintainability Grade | A | A | A | A |
| Halstead Volume | 262 | 250 | 250 | 266 |
| Halstead Difficulty | 4.2 | 4.4 | 4.4 | 4.7 |
| Halstead Bugs (est.) | 0.09 | 0.08 | 0.08 | 0.09 |
| Total Imports | 9 | 14 | 12 | 9 |
| Framework Imports | 1 | 4 | 2 | 0 |
| Classes | 1 | 2 | 1 | 1 |
| Functions | 9 | 12 | 9 | 9 |
| Type Annotation Coverage | 100% | 92% | 100% | 100% |

## Per-Question Results

### q1: What is the GIL in Python and how does it affect concurrency?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 9.84 | 5.49 | 4.55 | 11.27 |
| Tokens | 1,052 | 989 | 861 | 1,876 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 4 | 4 | 4 | 4 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: The GIL (Global Interpreter Lock) in CPython is a mutex that allows only one thread to execute Python bytecode at a time. Because of this, threads cannot achieve true parallelism for CPU-bound work—CPU-bound tasks do not benefit from threading. The GIL is released during I/O operations (file reads, ...
- **LangGraph**: The Global Interpreter Lock (GIL) in CPython is a mutex that allows only one thread to execute Python bytecode at a time. As a result, threads cannot achieve true parallelism for CPU-bound work—CPU-bound tasks do not benefit from threading under CPython. However, the GIL is released during I/O opera...
- **smolagents**: The GIL (Global Interpreter Lock) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. Because of this, threads cannot achieve true parallelism for CPU-bound work — CPU-heavy tasks do not benefit from threading under the GIL. The GIL is released during I/O operatio...
- **CrewAI**: CPython has a Global Interpreter Lock (GIL), a mutex that allows only one thread to execute Python bytecode at a time. This means that CPU-bound tasks do not benefit from threading in CPython. The GIL is released during I/O operations (file reads, network calls, etc.), so I/O-bound tasks can still b...

### q2: What is the difference between a 301 and a 302 HTTP redirect?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 5.46 | 4.03 | 5.64 | 8.83 |
| Tokens | 925 | 793 | 855 | 3,424 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: - 301 Moved Permanently — the resource has permanently moved to a new URL; clients and search engines should update their references (http_status_codes.md).  
- 302 Found — a temporary redirect: the resource is temporarily at a different URL and the client should continue using the original URL for ...
- **LangGraph**: - 301 Moved Permanently — the resource has permanently moved to a new URL; clients and search engines should update their references (http_status_codes.md).  
- 302 Found — the resource is temporarily at a different URL; the client should continue using the original URL for future requests (http_sta...
- **smolagents**: 301 Moved Permanently: the resource has permanently moved to a new URL — clients and search engines should update their references.  
302 Found: a temporary redirect — the resource is temporarily at a different URL, and the client should continue using the original URL for future requests.  

Source...
- **CrewAI**: "301 Moved Permanently means the resource has permanently moved to a new URL. Clients and search engines should update their references." (Source: http_status_codes.md)

"`302 Found` (commonly used as a temporary redirect) means the resource is temporarily at a different URL, and the client should c...

### q3: When should I use git rebase instead of git merge?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 5.76 | 5.38 | 4.16 | 10.44 |
| Tokens | 1,050 | 904 | 831 | 5,090 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: Use git rebase when you want to keep a feature branch up-to-date with main and produce a linear, cleaner commit history. Rebase "replays commits from one branch onto another," which results in a cleaner, easier-to-read commit log — so it's appropriate for updating a local feature branch before you m...
- **LangGraph**: Use rebase when you want to keep a feature branch up to date with main and produce a linear, cleaner commit history — e.g., replay your feature-branch commits onto `main` before merging (this makes the commit log easier to read) (git_branching.md).  

Do not rebase commits that have already been pus...
- **smolagents**: Use git rebase when you want to keep a feature branch up to date with main and produce a clean, linear commit history—e.g., replay your feature-branch commits onto main before merging to make the commit log easier to read. Do NOT rebase commits that have already been pushed to a shared branch, becau...
- **CrewAI**: [Source: git_branching.md]

## Merge vs Rebase

**Merge** creates a merge commit that preserves the full branch history. It is non-destructive and safe for shared branches. Use merge for pull requests and when you want a clear record of when branches were integrated.

**Rebase** replays commits from...

### q4: Should I use threading or asyncio for making many HTTP requests in Python?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 6.82 | 7.91 | 5.91 | 12.66 |
| Tokens | 961 | 989 | 995 | 6,817 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 4 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: Use asyncio for high-concurrency HTTP workloads; use threading for smaller-scale I/O when you want simpler, synchronous code.

- asyncio: best for high-concurrency I/O (e.g., thousands of simultaneous HTTP requests). It has very low overhead compared to threads but requires async/await throughout an...
- **LangGraph**: Short answer: use asyncio for high‑concurrency HTTP workloads; use threading only for smaller-scale, simpler cases. (Source: python_concurrency.md)

Why:
- Threading: “best for I/O-bound tasks like making HTTP requests… Threading is simpler to use for small‑scale concurrent I/O because it does not r...
- **smolagents**: Short answer: use asyncio if you need high concurrency (many, e.g. thousands, of simultaneous requests); use threading for simpler, smaller-scale I/O when you don't want to convert your code to async or your HTTP library has no async API.

Why: threading is good for I/O-bound work like HTTP requests...
- **CrewAI**: Threading (from python_concurrency.md):
"Python's `threading` module creates OS-level threads that share the same memory space. Threading is best for I/O-bound tasks like making HTTP requests, reading files, or database queries. Because of the GIL, threads cannot achieve true parallelism for CPU-bou...

### q5: What HTTP status code should a server return when a resource is not found?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 4.78 | 6.34 | 6.44 | 9.61 |
| Tokens | 797 | 931 | 777 | 8,151 |
| Correctness | 1 | 1 | 1 | 1 |
| Completeness | 1 | 1 | 1 | 1 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: I can't answer from the provided context. The excerpts from http_status_codes.md describe several status-code categories and examples (100, 200, 201, 204, 301, 302, 304, 400, 401) but do not state which code corresponds to "resource not found." (Source: http_status_codes.md)
- **LangGraph**: I can’t find the specific status code for "resource not found" in the provided excerpts — the 4xx section in http_status_codes.md is truncated and does not show the `404 Not Found` entry. (Source: http_status_codes.md)

If you want an answer based on general HTTP knowledge rather than only the provi...
- **smolagents**: I can't answer from the provided excerpts — the snippets show 4xx client errors and mention `400 Bad Request` and `401 Unauthorized`, but they do not include the status code for a resource not found. (Source: http_status_codes.md)
- **CrewAI**: I cannot answer from the provided context. The supplied excerpts from http_status_codes.md do not include the status code for "resource not found" (the 4xx section is truncated and only shows `400 Bad Request` and the start of `401 Unauthorized`). Source: http_status_codes.md

### q6: Explain the GitHub Flow branching strategy.

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 5.35 | 4.84 | 4.13 | 7.28 |
| Tokens | 735 | 805 | 809 | 9,517 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: GitHub Flow is a lightweight branching model for continuous deployment: create a feature branch from main, make commits, open a pull request for code review, and merge back into main after approval. The main branch is kept always deployable; there are no separate release or develop branches. This si...
- **LangGraph**: GitHub Flow is a lightweight branching model for continuous deployment. The workflow: create a feature branch from main, make commits, open a pull request for code review, and merge back into main after approval. The main branch is always kept deployable; there are no separate release or develop bra...
- **smolagents**: GitHub Flow (git_branching.md)

- Create a short-lived feature branch from main.
- Make commits on the feature branch.
- Open a pull request for code review.
- Merge the PR back into main after approval.

Characteristics: main is always deployable; there are no separate release or develop branches; ...
- **CrewAI**: ## GitHub Flow

GitHub Flow is a lightweight branching model designed for continuous deployment. The rules are simple: create a feature branch from `main`, make commits, open a pull request for code review, and merge back to `main` after approval. The `main` branch is always deployable. There are no...

### q7: What are the tradeoffs between multiprocessing and asyncio in Python?

| Metric | Pydantic AI | LangGraph | smolagents | CrewAI |
| --- | --- | --- | --- | --- |
| Latency (s) | 6.96 | 7.26 | 9.73 | 11.79 |
| Tokens | 1,057 | 1,128 | 1,421 | 11,464 |
| Correctness | 5 | 5 | 5 | 5 |
| Completeness | 5 | 5 | 5 | 5 |
| Faithfulness | 5 | 5 | 5 | 5 |
| Retrieval Prec | 1.00 | 1.00 | 1.00 | 1.00 |
| Retrieval Recall | 1.00 | 1.00 | 1.00 | 1.00 |

**Answers:**

- **Pydantic AI**: Short version — choose multiprocessing for CPU-bound work and asyncio for high-concurrency I/O, because their tradeoffs differ:

- Multiprocessing
  - Pros: bypasses the GIL (each process has its own interpreter/memory) so it’s ideal for CPU-bound tasks (data processing, heavy computation, image man...
- **LangGraph**: Short answer — tradeoffs:

- Multiprocessing
  - Pros: bypasses the GIL because each worker is a separate OS process with its own interpreter and memory, so it’s ideal for CPU-bound work (data processing, heavy computation, image work). (python_concurrency.md)
  - Cons: higher memory overhead (each ...
- **smolagents**: Short answer: use multiprocessing for CPU-bound work and asyncio for high‑concurrency I/O — each has clear tradeoffs.

- Multiprocessing — pros: bypasses the GIL (separate OS processes, each with its own interpreter), so it’s ideal for CPU‑bound tasks (data processing, math, image work). cons: highe...
- **CrewAI**: Based only on the provided context (python_concurrency.md):

Quoted context:
- "The `multiprocessing` module spawns separate OS processes, each with its own Python interpreter and memory space. This bypasses the GIL entirely, making it ideal for CPU-bound tasks like data processing, mathematical com...
