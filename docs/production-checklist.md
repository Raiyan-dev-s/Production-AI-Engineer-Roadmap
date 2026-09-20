# Production Checklist

A comprehensive checklist for shipping AI applications to production.

## Code Quality

### Architecture
- [ ] Clear separation of concerns (routes, services, models)
- [ ] Business logic not in API routes
- [ ] Configuration via environment variables
- [ ] Dependency injection where appropriate
- [ ] No circular imports

### Input Validation
- [ ] All user inputs validated with Pydantic
- [ ] Request body size limits
- [ ] SQL injection prevention (use ORM)
- [ ] File upload validation

### Error Handling
- [ ] No unhandled exceptions in routes
- [ ] Meaningful error responses
- [ ] Error logging with context
- [ ] Graceful degradation for non-critical failures

### Testing
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Test coverage >80% on core logic
- [ ] Tests run in CI on every PR

## AI/LLM

### Model Selection
- [ ] Model chosen based on task requirements
- [ ] Cost/performance trade-off documented
- [ ] Fallback model identified
- [ ] Model version pinned (not using "latest")

### Prompt Management
- [ ] Prompts version-controlled
- [ ] Prompts separate from code where possible
- [ ] System prompts tested for injection attacks
- [ ] Output format documented

### Evaluation
- [ ] Evaluation dataset created
- [ ] Baseline metrics established
- [ ] Evaluation runs automatically in CI
- [ ] Quality thresholds defined

### Hallucination Mitigation
- [ ] RAG used when domain-specific knowledge needed
- [ ] Output validation where applicable
- [ ] Confidence scoring implemented
- [ ] Fallback responses for low-confidence answers

### Cost Management
- [ ] Token usage tracked
- [ ] Cost alerts configured
- [ ] Caching implemented for repeated queries
- [ ] Prompt length optimized

## Security

### Secrets
- [ ] No secrets in code
- [ ] `.env` in `.gitignore`
- [ ] Production secrets managed via platform
- [ ] Secrets rotated regularly

### Authentication
- [ ] API authentication required
- [ ] Token validation on every request
- [ ] Rate limiting implemented
- [ ] CORS configured properly

### Data Protection
- [ ] HTTPS enforced
- [ ] PII handling documented
- [ ] Data retention policy defined
- [ ] Prompt injection testing done

## Infrastructure

### Docker
- [ ] Dockerfile uses multi-stage build
- [ ] Non-root user in container
- [ ] Health check endpoint defined
- [ ] Image size optimized

### CI/CD
- [ ] Tests run on every PR
- [ ] Linter and type checker run in CI
- [ ] Deployment automated
- [ ] Rollback process defined

### Deployment
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Health check endpoint working
- [ ] Logging configured

### Logging
- [ ] Structured logging (JSON)
- [ ] Request ID tracking
- [ ] Error logging with context
- [ ] No sensitive data in logs

### Monitoring
- [ ] Health check endpoint
- [ ] Error rate monitoring
- [ ] Latency tracking
- [ ] LLM cost tracking

## Performance

### Caching
- [ ] Response caching where appropriate
- [ ] LLM completion caching
- [ ] Embedding caching
- [ ] Cache invalidation strategy defined

### Latency
- [ ] Streaming responses for long operations
- [ ] Async I/O for database and HTTP calls
- [ ] Connection pooling configured
- [ ] Timeout values set appropriately

### Database
- [ ] Connection pooling configured
- [ ] Queries optimized (no N+1)
- [ ] Indexes on frequently queried columns
- [ ] Database backups configured

## Reliability

### Retries
- [ ] Retry logic for transient failures
- [ ] Exponential backoff implemented
- [ ] Maximum retry limits set
- [ ] Circuit breaker for external services

### Timeouts
- [ ] HTTP client timeouts set
- [ ] Database query timeouts set
- [ ] LLM API timeouts set
- [ ] Background task timeouts set

### Graceful Failure
- [ ] Fallback responses for LLM failures
- [ ] Default values for missing data
- [ ] User-friendly error messages
- [ ] Partial results returned when possible

### Observability
- [ ] Request tracing implemented
- [ ] Performance metrics collected
- [ ] Error tracking configured
- [ ] Dashboard for key metrics
