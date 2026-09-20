# Testing

## Testing Philosophy

**Write tests that catch real bugs.** Not 100% coverage for its own sake, but tests that give you confidence to change code.

## Test Types

### Unit Tests

Test individual functions and classes in isolation.

```python
def test_parse_llm_response():
    response = parse_llm_response('{"answer": "42"}')
    assert response.answer == "42"


def test_parse_llm_response_invalid_json():
    with pytest.raises(ValueError):
        parse_llm_response("not json")
```

- **Fast** — runs in milliseconds
- **Isolated** — no external dependencies (network, database, LLM)
- **Many** — most of your tests should be unit tests

### Integration Tests

Test multiple components working together.

```python
@pytest.mark.integration
async def test_create_user_in_db():
    async with async_session() as session:
        user = User(name="test", email="test@example.com")
        session.add(user)
        await session.commit()
        result = await session.get(User, user.id)
        assert result.name == "test"
```

- **Slower** — may involve database or API calls
- **Realistic** — tests real interactions
- **Fewer** — write enough to cover critical paths

### End-to-End (E2E) Tests

Test the full application from user perspective.

```python
@pytest.mark.integration
async def test_api_create_user():
    response = await client.post("/users", json={"name": "test"})
    assert response.status_code == 200
    assert response.json()["name"] == "test"
```

- **Slowest** — tests the whole stack
- **Most realistic** — tests what users actually do
- **Least** — write only for critical user flows

## Pytest Patterns

### Fixtures

```python
@pytest.fixture
def sample_user():
    return User(name="test", email="test@example.com")


@pytest.fixture
async def db_session():
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def mock_llm(monkeypatch):
    async def mock_complete(*args, **kwargs):
        return LLMResponse(content="mocked response")

    monkeypatch.setattr("app.llm.complete", mock_complete)
```

### Parametrize

```python
@pytest.mark.parametrize(
    "input,expected",
    [
        ("hello", "HELLO"),
        ("world", "WORLD"),
        ("", ""),
    ],
)
def test_to_uppercase(input, expected):
    assert to_uppercase(input) == expected
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Markers

```python
@pytest.mark.slow
def test_expensive_operation(): ...


@pytest.mark.integration
async def test_with_database(): ...
```

## Mocking

```python
from unittest.mock import AsyncMock, patch


# Mock an LLM call
@patch("app.services.llm.client.chat.completions.create")
async def test_with_mocked_llm(mock_create):
    mock_create.return_value = AsyncMock(
        choices=[AsyncMock(message=AsyncMock(content="test"))]
    )
    result = await call_llm("hello")
    assert result == "test"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run only unit tests
pytest -m "not integration"

# Run specific file
pytest tests/test_auth.py

# Verbose output
pytest -v
```

## Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=term-missing

# HTML report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

Aim for >80% coverage on business logic. Don't chase 100% — focus on catching real bugs.
