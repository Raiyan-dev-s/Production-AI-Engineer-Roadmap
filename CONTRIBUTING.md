# Contributing to Production AI Engineering

Thank you for your interest in contributing! This guide will help you get started.

## Branch Naming

Use descriptive branch names with prefixes:

- `feature/` — new features
- `fix/` — bug fixes
- `docs/` — documentation changes
- `refactor/` — code refactoring
- `test/` — adding or updating tests

Example: `feature/add-rag-chunking`

## Commit Messages

Follow Conventional Commits:

```
type(scope): description

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(api): add user registration endpoint`
- `docs: update production checklist`
- `fix(rag): handle empty document chunks`

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes
3. Run linting, type checking, and tests
4. Push and create a pull request
5. Fill in the PR description with what changed and why

## Code Quality

Before committing, run:

```bash
ruff check .
ruff format .
mypy .
pytest
```

All checks must pass before submitting a PR.

## Testing

- Write tests for new functionality
- Ensure existing tests still pass
- Aim for meaningful coverage, not 100% line coverage

## Documentation

- Update README if adding new features
- Add docstrings to public functions
- Keep documentation beginner-friendly
