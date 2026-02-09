# Python Concurrency Models

Python offers three main approaches to concurrent execution: threading, multiprocessing, and asyncio. Each has distinct tradeoffs.

## The Global Interpreter Lock (GIL)

CPython has a Global Interpreter Lock (GIL), a mutex that allows only one thread to execute Python bytecode at a time. This means that CPU-bound tasks do not benefit from threading in CPython. The GIL is released during I/O operations (file reads, network calls, etc.), so I/O-bound tasks can still benefit from threading.

## Threading

Python's `threading` module creates OS-level threads that share the same memory space. Threading is best for I/O-bound tasks like making HTTP requests, reading files, or database queries. Because of the GIL, threads cannot achieve true parallelism for CPU-bound work. Threading is simpler to use for small-scale concurrent I/O because it does not require restructuring your code with async/await.

## Multiprocessing

The `multiprocessing` module spawns separate OS processes, each with its own Python interpreter and memory space. This bypasses the GIL entirely, making it ideal for CPU-bound tasks like data processing, mathematical computations, or image manipulation. The tradeoff is higher memory overhead (each process has its own memory) and more complex inter-process communication (IPC) via queues, pipes, or shared memory.

## Asyncio

`asyncio` uses a single-threaded event loop with cooperative multitasking. Functions are defined with `async def` and yield control with `await`. It is best for high-concurrency I/O-bound tasks, like handling thousands of simultaneous HTTP requests or WebSocket connections. The overhead is very low compared to threading. However, asyncio requires the entire call chain to use async/await syntax, which means all libraries must support async interfaces.

## When to Use Each

- **CPU-bound work**: Use `multiprocessing` to bypass the GIL.
- **Small-scale I/O**: Use `threading` for simplicity.
- **High-concurrency I/O**: Use `asyncio` for efficiency with minimal overhead.
- **Mixed workloads**: Combine `asyncio` with `ProcessPoolExecutor` for I/O orchestration with CPU-bound processing.
