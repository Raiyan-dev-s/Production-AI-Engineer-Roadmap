# Security Checklist

Beginner-friendly security practices for AI applications.

## Secrets Management

- [ ] Never commit `.env` files to git
- [ ] Use `.env.example` as documentation (no real values)
- [ ] Use platform secrets for production (GitHub Actions, AWS SSM, etc.)
- [ ] Rotate API keys and secrets regularly
- [ ] Use different secrets for dev/staging/production
- [ ] Never log secrets or API keys

```python
# Good - uses environment variable
api_key = os.environ["OPENAI_API_KEY"]

# Bad - hardcoded secret
api_key = "sk-1234567890abcdef"
```

## Authentication & Authorization

- [ ] Use API keys or JWT tokens for authentication
- [ ] Validate tokens on every request
- [ ] Use HTTPS in production (never HTTP)
- [ ] Implement rate limiting
- [ ] Use short-lived tokens (15 min for access, 7 days for refresh)

## Input Validation

- [ ] Validate all user input with Pydantic
- [ ] Reject unexpected fields
- [ ] Limit input length
- [ ] Sanitize text before passing to LLM

```python
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., max_length=1000)
    model: str = Field(default="gpt-4o", pattern="^(gpt-4o|gpt-3.5-turbo)$")
```

## Rate Limiting

- [ ] Limit requests per user/IP
- [ ] Limit LLM calls per user
- [ ] Implement exponential backoff for retries

## Prompt Injection Protection

- [ ] Never pass raw user input directly to LLM as system prompts
- [ ] Use input sanitization
- [ ] Separate user content from instructions
- [ ] Test with adversarial inputs

```python
# Good - user content is clearly separated
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Answer based on the context.",
    },
    {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"},
]

# Bad - user input could override system instructions
messages = [
    {
        "role": "user",
        "content": user_input,
    }  # user could say "ignore previous instructions..."
]
```

## API Key Protection

- [ ] Never expose API keys in client-side code
- [ ] Never include API keys in URLs
- [ ] Never log API keys
- [ ] Use environment variables, not config files

## Data Protection

- [ ] Encrypt sensitive data at rest
- [ ] Use HTTPS for data in transit
- [ ] Don't store unnecessary user data
- [ ] Implement data retention policies
- [ ] Be careful with PII in LLM prompts

## Logging

- [ ] Log authentication events
- [ ] Log errors (but not secrets)
- [ ] Log API usage for auditing
- [ ] Never log user passwords or tokens

```python
# Good - logs the event without sensitive data
logger.info("user_login", user_id=user.id, ip=request.client.host)

# Bad - logs sensitive information
logger.info("user_login", email=user.email, password=user.password)
```

## Dependency Security

- [ ] Keep dependencies updated
- [ ] Use `pip-audit` or similar to scan for vulnerabilities
- [ ] Pin dependency versions
- [ ] Review dependencies before adding new ones

## Quick Security Audit

```bash
# Check for hardcoded secrets
grep -r "sk-" . --include="*.py"
grep -r "api_key" . --include="*.py"
grep -r "password" . --include="*.py"

# Check for .env in git
git ls-files | grep "\.env$"

# Audit dependencies
pip-audit
```
