# Deployment

## Overview

Getting your application from development to production safely and reliably.

## Docker

### Dockerfile

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t myapp .

# Run container
docker run -p 8000:8000 --env-file .env myapp
```

### Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

## Environment Variables

### Management

- **Development**: `.env` file (never commit this)
- **Staging/Production**: platform secrets (GitHub Actions secrets, AWS SSM, etc.)
- **Principle**: never hardcode secrets, never log them

### Validation

Use Pydantic to validate required environment variables at startup:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    openai_api_key: str | None = None

    model_config = {"env_file": ".env"}
```

## Secrets Management

- Use `.env` files for local development
- Use platform-managed secrets for production
- Never commit secrets to git
- Rotate secrets regularly
- Use `.env.example` as documentation

## CI/CD

### GitHub Actions Example

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy .
      - run: pytest

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploy your app here"
```

## Cloud Options

| Platform | Complexity | Cost | Best For |
|----------|-----------|------|----------|
| Railway | Low | Low | Small projects, prototypes |
| Render | Low | Low | Simple web services |
| AWS (EC2/ECS) | Medium | Medium | Production apps |
| GCP (Cloud Run) | Medium | Medium | Container-based apps |
| Kubernetes | High | Variable | Large-scale systems |

## Zero-Downtime Deploys

- **Rolling updates**: replace instances one at a time
- **Blue-green**: deploy new version alongside old, switch traffic
- **Health checks**: verify new instances are ready before routing traffic

## Logging

```python
import structlog

logger = structlog.get_logger()

logger.info("user_created", user_id=user.id, email=user.email)
logger.error("llm_call_failed", error=str(error), model="gpt-4")
```

Structured logs (JSON) are easier to search and analyze in production.

## Health Checks

```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

Use this endpoint for container orchestration health checks.
