# Backend Engineering

## What to Learn

Building reliable HTTP APIs and services — the backbone that serves AI models and handles user requests.

## Why It Matters

An AI model without a solid backend is a notebook. Backend skills turn models into products that users can actually interact with.

## Concepts Checklist

- [ ] **HTTP Fundamentals**: methods (GET/POST/PUT/DELETE), status codes, headers, content types
- [ ] **REST API Design**: resource naming, HTTP verbs, consistent response shapes
- [ ] **Request Validation**: Pydantic models, input sanitization, error responses
- [ ] **Authentication & Authorization**: API keys, JWT tokens, OAuth2 basics
- [ ] **Middleware**: request/response processing pipeline, CORS, logging
- [ ] **Database ORM**: SQLAlchemy models, queries, relationships, async sessions
- [ ] **Migrations**: Alembic for schema changes, version control for your database
- [ ] **Background Tasks**: task queues, async job processing, retry logic
- [ ] **Caching**: Redis basics, cache invalidation strategies, when to cache
- [ ] **Rate Limiting**: protecting your API from abuse
- [ ] **WebSockets**: real-time communication patterns

## Practice Suggestions

1. **Build a CRUD API** — a FastAPI service with Pydantic models, SQLAlchemy ORM, and proper error handling. Add pagination.
2. **Add auth to an existing API** — implement API key authentication with middleware, and protect certain endpoints.

## Completion Checklist

- [ ] Can design a REST API with proper URL naming and status codes
- [ ] Can write Pydantic models for request/response validation
- [ ] Understands JWT authentication flow
- [ ] Can use SQLAlchemy for database operations
- [ ] Has used Alembic for at least one migration
- [ ] Knows when and how to add caching
