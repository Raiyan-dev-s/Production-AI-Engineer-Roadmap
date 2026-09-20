# Python Fundamentals

## What to Learn

Core Python skills needed for production AI engineering — not just "writing scripts," but writing reliable, maintainable code.

## Why It Matters

Python is the lingua franca of AI/ML. Poor Python fundamentals lead to brittle code, subtle bugs, and difficulty reading other people's libraries.

## Concepts Checklist

- [ ] **Types & Data Structures**: `int`, `float`, `str`, `bool`, `list`, `dict`, `tuple`, `set`, `None`
- [ ] **Comprehensions**: list/dict/set comprehensions for concise data transforms
- [ ] **Functions**: positional/keyword args, `*args`/`**kwargs`, return values, closures
- [ ] **Decorators**: writing and applying function/class decorators
- [ ] **Generators & Iterators**: `yield`, lazy evaluation, memory-efficient pipelines
- [ ] **OOP**: classes, inheritance, `dataclasses`, `__init__`, `__repr__`, protocols
- [ ] **Async/Await**: `asyncio`, `async def`, `await`, async context managers
- [ ] **Type Hints**: function signatures, `Optional`, `Union`, `TypeVar`, `Protocol`
- [ ] **Virtual Environments**: `venv`, `uv`, dependency isolation
- [ ] **Packaging**: `pyproject.toml`, `pip install -e .`, entry points, versioning
- [ ] **Error Handling**: `try/except/finally`, custom exceptions, exception chaining
- [ ] **Context Managers**: `with` statement, `contextlib`

## Practice Suggestions

1. **Build a CLI tool** — a small command-line utility that reads a file, transforms data, and writes output. Use type hints, a dataclass for config, and proper error handling.
2. **Write an async downloader** — fetch multiple URLs concurrently using `httpx` and `asyncio`. Compare performance to sequential requests.

## Completion Checklist

- [ ] Can write functions with proper type hints
- [ ] Understands when to use generators vs lists
- [ ] Can write and use decorators
- [ ] Comfortable with async/await patterns
- [ ] Can set up a venv and manage dependencies
- [ ] Can create a `pyproject.toml`-based package
- [ ] Writes code that passes `ruff check` and `mypy --strict`
