# Production AI Engineering

A monorepo for learning and building production-ready AI applications.

## What Is This Repository?

This is a **learning + project workspace** — not a finished application. Each project is an independent, runnable application with its own dependencies and tests.

Use it to:
- Learn Production AI Engineering step by step
- Practice building real projects with proper architecture
- Reference production patterns and best practices
- Organize your AI learning journey

## Projects

| Project | Description | Status |
|---------|-------------|--------|
| [01-rest-api](projects/01-rest-api/) | FastAPI with Route → Service → Repository → Database | Runnable |
| [02-llm-app](projects/02-llm-app/) | LLM integration with pluggable provider pattern | Runnable |
| [03-rag-app](projects/03-rag-app/) | Retrieval-Augmented Generation | Scaffold |
| [04-ai-agent](projects/04-ai-agent/) | Agent with tools and reasoning | Scaffold |
| [05-production-ai-system](projects/05-production-ai-system/) | Full production AI system | Scaffold |

## Monorepo Structure

```
ai-production-kit/
├── projects/
│   ├── 01-rest-api/       # Each project has its own pyproject.toml,
│   ├── 02-llm-app/        #   requirements.txt, tests, and README
│   ├── 03-rag-app/
│   ├── 04-ai-agent/
│   └── 05-production-ai-system/
├── pyproject.toml          # Root: ruff config only (workspace-level)
├── .github/workflows/ci.yml
└── README.md
```

Each project is **self-contained** — run it from its own directory with its own virtual environment.

## Quick Start

```bash
git clone <your-repo-url>
cd ai-production-kit
```

### Running a Project

```bash
# Pick any project
cd projects/01-rest-api

# Create virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

### Running Tests

```bash
# From the project directory
cd projects/01-rest-api
pip install -r requirements.txt
pytest -v

# Or from the repo root (CI uses working-directory)
cd projects/01-rest-api && pytest tests/ -v
```

## Development

### Linting (from repo root)

```bash
pip install ruff
ruff check .
ruff format --check .
```

### Type Checking (from project directory)

```bash
cd projects/01-rest-api
pip install mypy
mypy . --ignore-missing-imports
```

## CI

GitHub Actions runs per-project jobs. Each project is tested independently from its own directory:

- **lint** — Ruff from repo root
- **project-01** — Lint, type check, test for REST API
- **project-02** — Lint, type check, test for LLM App

## Learning Path

```
Python
   ↓
Backend & APIs (01-rest-api)
   ↓
LLM Applications (02-llm-app)
   ↓
RAG (03-rag-app)
   ↓
AI Agents (04-ai-agent)
   ↓
Production Systems (05-production-ai-system)
```

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | Architecture patterns and decisions |
| [Environment Setup](docs/environment-setup.md) | Detailed local setup guide |
| [Git Workflow](docs/git-workflow.md) | Git branching and commit conventions |
| [Testing Guide](docs/testing.md) | Testing philosophy and patterns |
| [Deployment](docs/deployment.md) | Deployment concepts and practices |
| [Security Checklist](docs/security-checklist.md) | Security best practices |
| [Production Checklist](docs/production-checklist.md) | Production readiness checklist |

## License

MIT License — see [LICENSE](LICENSE) for details.
