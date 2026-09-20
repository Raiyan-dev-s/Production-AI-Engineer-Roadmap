# Production AI Engineering

A professional workspace for learning and building production-ready AI applications.

## What Is This Repository?

This is a **learning + project workspace** — not a finished application. It provides a clean, reusable structure that teaches beginners how real AI projects should be organized.

Use it to:
- Learn Production AI Engineering step by step
- Practice building real projects with proper architecture
- Reference production patterns and best practices
- Organize your AI learning journey

## Who Is This For?

- Developers transitioning into AI engineering
- ML engineers who want to learn production practices
- Backend developers adding AI to their skill set
- Anyone who wants to build AI systems that actually work in production

## What Is Production AI Engineering?

Production AI Engineering is the discipline of building AI applications that are:

- **Reliable** — they handle failures gracefully
- **Scalable** — they work under real-world load
- **Maintainable** — clean code, good architecture, proper testing
- **Secure** — secrets management, input validation, prompt injection protection
- **Observable** — logging, monitoring, metrics, tracing

It's the difference between a Jupyter notebook demo and a system you'd trust with real users.

## Learning Path

```
Python
   ↓
Backend & APIs
   ↓
LLM Applications
   ↓
RAG
   ↓
AI Agents
   ↓
Production AI Systems
```

Each area builds on the previous one. Start with Python fundamentals, progress through backend engineering, then into AI-specific patterns.

### Learning Areas

| Area | Directory | What You'll Learn |
|------|-----------|-------------------|
| Python | `learning/python/` | Types, async, packaging, best practices |
| Backend | `learning/backend/` | HTTP, APIs, databases, authentication |
| LLM | `learning/llm/` | LLM APIs, prompts, streaming, cost |
| RAG | `learning/rag/` | Retrieval, embeddings, vector stores |
| Agents | `learning/agents/` | Tool use, reasoning loops, orchestration |
| Databases | `learning/databases/` | SQL, ORMs, caching, vector DBs |
| Deployment | `learning/deployment/` | Docker, CI/CD, monitoring |

## Project Progression

Each project increases in complexity and production-orientation:

| Project | Description | Type |
|---------|-------------|------|
| [01-rest-api](projects/01-rest-api/) | FastAPI with clean architecture | Runnable |
| [02-llm-app](projects/02-llm-app/) | LLM integration with provider pattern | Runnable |
| [03-rag-app](projects/03-rag-app/) | Retrieval-Augmented Generation | Scaffold |
| [04-ai-agent](projects/04-ai-agent/) | Agent with tools and reasoning | Scaffold |
| [05-production-ai-system](projects/05-production-ai-system/) | Full production AI system | Scaffold |

## Local Setup

### Prerequisites

- Python 3.12+
- Git

### Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd production-ai-engineering

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Copy environment variables
cp .env.example .env

# Run linting and tests
ruff check .
pytest
```

### Running Project 01 (REST API)

```bash
cd projects/01-rest-api
pip install -r requirements.txt
uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

### Running Project 02 (LLM App)

```bash
cd projects/02-llm-app
pip install -r requirements.txt
uvicorn app.main:app --reload
# Works with mock provider out of the box
```

## Environment Variables

Copy `.env.example` to `.env` and fill in values as needed:

```bash
cp .env.example .env
```

Variables are optional unless noted. Projects work with sensible defaults for local development.

## Development Commands

```bash
# Linting
ruff check .           # Check for issues
ruff check --fix .     # Auto-fix issues
ruff format .          # Format code

# Type checking
mypy .

# Testing
pytest                  # Run all tests
pytest -v               # Verbose output
pytest --cov            # With coverage
pytest -m "not slow"    # Skip slow tests
```

## Testing

Tests use pytest. Each project has its own `tests/` directory.

```bash
# Run all tests
pytest

# Run specific project tests
pytest projects/01-rest-api/tests/

# Run with coverage
pytest --cov --cov-report=html
```

## Code Quality

This repository enforces:

- **Ruff** for linting and formatting (replaces flake8, isort, black)
- **mypy** for static type checking
- **pytest** for testing
- **Pre-commit hooks** (optional)

All checks run automatically in CI on every push and pull request.

## Docker

Project 01 includes a Docker setup:

```bash
cd projects/01-rest-api

# Build
docker build -t rest-api .

# Run
docker run -p 8000:8000 rest-api

# Or use docker-compose
docker-compose up
```

## Deployment

See `docs/deployment.md` for deployment concepts. This repository provides:

- Dockerfiles ready for container deployment
- CI/CD via GitHub Actions
- Environment-based configuration
- Health check endpoints

## Git Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit with clear messages
3. Push and create a pull request
4. CI runs automatically
5. Merge after review

See `CONTRIBUTING.md` for detailed guidelines.

## Repository Philosophy

**Clean** — No unnecessary complexity
**Professional** — Real production patterns
**Beginner-friendly** — Clear code with purpose
**Practical** — Focus on what matters in production
**Reusable** — Start any AI project from this structure

## What This Is NOT

- A finished application to deploy as-is
- A collection of tutorials or courses
- A framework or library
- A competition leaderboard

It is a **workspace and reference** for learning Production AI Engineering.

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | Architecture patterns and decisions |
| [Environment Setup](docs/environment-setup.md) | Detailed local setup guide |
| [Git Workflow](docs/git-workflow.md) | Git branching and commit conventions |
| [Testing Guide](docs/testing.md) | Testing philosophy and patterns |
| [Deployment](docs/deployment.md) | Deployment concepts and practices |
| [API Design](docs/api-design.md) | REST API design principles |
| [AI Architecture](docs/ai-application-architecture.md) | AI application patterns |
| [Security Checklist](docs/security-checklist.md) | Security best practices |
| [Production Checklist](docs/production-checklist.md) | Production readiness checklist |

## License

MIT License — see [LICENSE](LICENSE) for details.
