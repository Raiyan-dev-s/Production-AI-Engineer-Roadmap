# Databases

## What to Learn

Storing and retrieving data reliably — from traditional SQL databases to modern vector stores.

## Why It Matters

Every production application needs persistent storage. Choosing the right database and using it correctly determines whether your app scales or breaks.

## Concepts Checklist

- [ ] **SQL Basics**: SELECT, INSERT, UPDATE, DELETE, JOINs, GROUP BY, indexes
- [ ] **PostgreSQL**: installation, `psql`, schemas, data types, JSONB, full-text search
- [ ] **SQLite**: when to use it, file-based simplicity, limitations
- [ ] **ORMs**: SQLAlchemy models, relationships (one-to-many, many-to-many), sessions
- [ ] **Migrations**: Alembic, schema version control, rolling back changes
- [ ] **Connection Pooling**: why it matters, SQLAlchemy pool configuration
- [ ] **Redis**: key-value caching, pub/sub, session storage, rate limiting
- [ ] **Vector Databases**: Chroma, Pinecone, Qdrant — storing embeddings for RAG
- [ ] **Query Optimization**: EXPLAIN, indexing strategies, N+1 query problems
- [ ] **Data Modeling**: normalization, denormalization, when to use each

## Practice Suggestions

1. **Build a schema** — design and implement a database schema for a simple application (blog, inventory, CRM). Include at least 3 tables with relationships. Run migrations.
2. **Add caching with Redis** — cache the results of expensive database queries. Implement cache invalidation when data changes.

## Completion Checklist

- [ ] Can write SQL queries for common operations
- [ ] Can design a normalized database schema
- [ ] Can use SQLAlchemy to interact with a database
- [ ] Has run Alembic migrations
- [ ] Understands connection pooling and why it matters
- [ ] Has used Redis for caching at least once
