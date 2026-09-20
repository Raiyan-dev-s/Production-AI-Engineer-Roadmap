# LLM Application

A production-ready LLM application demonstrating clean architecture with pluggable providers (Mock, OpenAI, Anthropic).

## What This Teaches

- Separation of concerns: API → Business Logic → LLM Service → Data layer
- Abstract base classes for pluggable provider architecture
- Factory pattern for provider selection
- Async/await throughout the stack
- Pydantic schemas for request/response validation
- Prompt template management
- Structured logging with structlog
- Clean error handling with custom exceptions

## Architecture

```
Request → FastAPI Router → Service Layer → LLM Provider → Response
                         ↑                  ↑
                   Prompt Templates    Abstract Base (ABC)
                                        ↓
                                  Mock | OpenAI | Anthropic
```

The layers are:

- **API Layer** (`app/api/routes/`) — HTTP endpoints, request validation, response formatting
- **Service Layer** (`app/services/`) — Business logic, prompt templates, orchestration
- **LLM Layer** (`app/llm/`) — Provider abstraction with abstract base class
- **Schema Layer** (`app/schemas/`) — Pydantic models for type-safe data exchange
- **Core Layer** (`app/core/`) — Configuration, exceptions, shared utilities

## Tech Stack

- **FastAPI** — Async web framework
- **Pydantic v2** — Data validation and settings management
- **structlog** — Structured logging
- **httpx** — Async HTTP client (for real provider integrations)
- **OpenAI SDK** — OpenAI provider (optional)
- **Anthropic SDK** — Anthropic provider (optional)

## Folder Structure

```
02-llm-app/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── chat.py          # POST /api/chat, /api/summarize, /api/classify, GET /api/models
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic Settings
│   │   └── exceptions.py        # Custom exceptions
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base class LLMProvider
│   │   ├── mock_provider.py     # Mock provider for dev/testing
│   │   ├── openai_provider.py   # OpenAI integration
│   │   ├── anthropic_provider.py # Anthropic integration
│   │   └── factory.py           # Provider factory
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── llm.py               # Pydantic request/response models
│   └── services/
│       ├── __init__.py
│       ├── chat.py              # ChatService: chat, summarize, classify
│       └── prompt_templates.py  # Prompt template dictionary
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures
│   ├── test_chat.py             # API endpoint tests
│   ├── test_llm_providers.py    # Provider unit tests
│   └── test_services.py         # Service unit tests
├── pyproject.toml               # Project config, ruff, mypy, pytest
├── requirements.txt
└── README.md
```

## Setup

```bash
cd projects/02-llm-app
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Application
APP_ENV=development
DEBUG=true

# LLM Provider (mock, openai, anthropic)
LLM_PROVIDER=mock

# Model settings
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=1024
TEMPERATURE=0.7

# API Keys (only needed for real providers)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## How to Run

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API docs are available at `http://localhost:8000/docs`.

## How to Test

```bash
# Run all tests
pytest -v

# Run with coverage
pytest -v --tb=short

# Run specific test file
pytest tests/test_chat.py -v
pytest tests/test_llm_providers.py -v
pytest tests/test_services.py -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/chat` | Chat completion |
| `POST` | `/api/summarize` | Text summarization |
| `POST` | `/api/classify` | Text classification |
| `GET` | `/api/models` | List available models |
| `GET` | `/health` | Health check |

## How to Switch to a Real Provider

1. Install the provider package:

```bash
# For OpenAI
pip install openai

# For Anthropic
pip install anthropic
```

2. Set your API key in `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4o
```

3. Restart the application. The factory will automatically instantiate the correct provider.

## Improvements

- Add Redis-backed rate limiting
- Add response caching with semantic similarity
- Implement token counting with tiktoken
- Add streaming support to the summarize/classify endpoints
- Add authentication and API key management
- Add request/response logging middleware
- Implement retry logic with exponential backoff
- Add health checks per provider
- Containerize with Docker
- Add OpenTelemetry tracing
