# REST API — Route → Service → Repository → Database

A beginner-friendly FastAPI project that demonstrates clean architecture with a
four-layer pattern: **Route → Service → Repository → Database**.

---

## Problem

Most tutorials show all logic crammed into route handlers. Real applications need
clear separation of concerns so that business logic, data access, and HTTP
handling can evolve independently. This project provides a small but complete
reference implementation.

## What it teaches

- FastAPI project structure with routers, services, and repositories
- Async Python with `async`/`await` throughout
- SQLAlchemy 2.0 async ORM with aiosqlite
- Pydantic v2 schemas for validation and serialization
- Dependency injection with FastAPI's `Depends`
- Structured logging with structlog
- Global exception handling
- Docker multi-stage build
- pytest async test suite with fixtures

## Architecture

```
Request → Route (HTTP layer)
             ↓
          Service (business logic)
             ↓
          Repository (data access)
             ↓
          Database (SQLAlchemy async)
```

Each layer has a single responsibility and depends only on the layer below it.

## Tech Stack

| Concern | Library |
|---|---|
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| Validation / config | Pydantic v2, pydantic-settings |
| ORM | SQLAlchemy 2.0 (async) |
| Database | SQLite via aiosqlite |
| HTTP client (tests) | httpx |
| Logging | structlog |
| Testing | pytest, pytest-asyncio |

## Folder Structure

```
01-rest-api/
├── app/
│   ├── api/routes/       # HTTP endpoint definitions
│   ├── core/             # Config, exceptions, logging
│   ├── database/         # Engine, session, base
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic layer
│   └── main.py           # App factory
├── tests/                # Async pytest suite
├── pyproject.toml        # Project config, ruff, mypy, pytest
├── requirements.txt      # Pip-compatible dependencies
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Setup

```bash
# Clone and enter the project
cd projects/01-rest-api

# Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | `development` or `production` |
| `DEBUG` | `true` | Enable Swagger/ReDoc docs |
| `DATABASE_URL` | `sqlite+aiosqlite:///./app.db` | Async database connection string |
| `SECRET_KEY` | `change-me-in-production` | Secret key for sessions/tokens |
| `LOG_LEVEL` | `INFO` | Structured log level |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins |

## How to Run

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at
`http://localhost:8000/docs`.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check with DB status |
| `GET` | `/api/items` | List items (paginated) |
| `GET` | `/api/items/{id}` | Get a single item |
| `POST` | `/api/items` | Create an item |
| `PUT` | `/api/items/{id}` | Update an item |
| `DELETE` | `/api/items/{id}` | Delete an item |

## How to Test

```bash
# Run all tests
pytest -v

# Run with coverage
pytest -v --tb=short
```

## Docker

```bash
docker compose up --build
```

## Possible Improvements

- Add PostgreSQL support (swap aiosqlite for asyncpg)
- Authentication and authorization (JWT / OAuth2)
- Alembic database migrations
- Request ID middleware for distributed tracing
- Rate limiting
- Pagination with cursor-based approach
- Full OpenAPI documentation with examples
- CI pipeline with linting (ruff) and type checking (mypy)
