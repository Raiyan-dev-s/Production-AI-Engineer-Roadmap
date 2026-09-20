# Production AI Architecture Patterns

## Overview

This document covers common architecture patterns for AI-powered applications — when to use which, and why.

## Layer Separation

A production AI application typically has these layers:

```
┌─────────────────────────────┐
│       Presentation          │  API endpoints, UI
├─────────────────────────────┤
│       Application           │  Business logic, orchestration
├─────────────────────────────┤
│       AI Services           │  LLM calls, embeddings, RAG
├─────────────────────────────┤
│       Data Layer            │  Database, cache, vector store
├─────────────────────────────┤
│       Infrastructure        │  Docker, CI/CD, monitoring
└─────────────────────────────┘
```

**Keep layers separate.** Don't put database queries in your API endpoints. Don't put business logic in your prompts.

## Common Patterns

### 1. Simple LLM API

```
User → API → LLM Provider → Response
```

Best for: chatbots, content generation, simple Q&A.
Complexity: Low.

### 2. RAG Pipeline

```
User → API → Retriever → Vector Store
                    ↓
              Context Builder → LLM → Response
```

Best for: document Q&A, knowledge bases.
Complexity: Medium.

### 3. Agent System

```
User → API → Agent Loop → Tools → LLM → Response
                ↑              ↓
                └──── Memory ──┘
```

Best for: complex multi-step tasks, autonomous workflows.
Complexity: High.

### 4. Hybrid (RAG + Agent)

```
User → API → Agent → RAG Pipeline
                ↓         ↓
            Tools    Vector Store
                ↓         ↓
              LLM → Response
```

Best for: enterprise applications with multiple data sources.
Complexity: High.

## When to Use What

| Need | Pattern | Complexity |
|------|---------|------------|
| Answer general questions | Simple LLM API | Low |
| Answer questions about your data | RAG | Medium |
| Perform multi-step tasks | Agent | High |
| Enterprise knowledge system | RAG + Agent | High |

## Anti-Patterns

- **Monolithic prompt**: one giant prompt doing everything. Split into focused components.
- **No error handling**: LLM calls fail, APIs timeout. Always handle failures.
- **No caching**: re-sending the same prompt repeatedly is slow and expensive.
- **Hardcoded model selection**: different tasks need different models. Abstract model selection.
- **No evaluation**: if you can't measure quality, you can't improve it.

## Key Principles

1. **Separate concerns** — business logic, AI logic, and data access should be in separate modules
2. **Design for failure** — every LLM call can fail; every tool call can timeout
3. **Cache aggressively** — embeddings, completions, and retrieval results are cacheable
4. **Evaluate continuously** — build evaluation sets early, run them often
5. **Start simple** — don't build an agent if a prompt will do
