# Project 05: Production AI System

A scaffold showing what a production-grade AI inference service looks like, addressing the concerns that go beyond model code.

## What a Production AI System Addresses

```
  Request
      |
      v
  +-----------+     +------------+     +------------+     +-----------+
  |   API     | --> | Validation | --> |Preprocessing| --> | Inference |
  | (FastAPI) |     | & Sanitize |     | & Batch    |     | (Model)   |
  +-----------+     +------------+     +------------+     +-----------+
      |                                                        |
      |              +------------+     +------------+         |
      +------------> | Postprocess| <-- |  Quality   | <-------+
                     | & Format   |     |  Check     |
                     +------------+     +------------+
                            |
                     +------------+     +------------+
                     | Monitoring |     |  Fallback  |
                     | & Metrics  |     | & Retry    |
                     +------------+     +------------+
                            |
                            v
                       Response

  Cross-cutting concerns:
  - Structured logging (every step)
  - Request tracing (request IDs)
  - Error handling (typed exceptions)
  - Health checks (liveness + readiness)
  - Metrics (latency, throughput, errors)
  - Graceful degradation (fallbacks)
```

## Architecture

```
app/
  main.py                   # FastAPI app with middleware stack
  core/
    config.py               # Pydantic Settings
    exceptions.py           # Typed exception hierarchy
  schemas/
    common.py               # StandardResponse, pagination, errors
  ai/
    model_manager.py        # Load, unload, track models
    pipeline.py             # Orchestrate: validate->preprocess->predict->postprocess
    evaluation.py           # Quality checks and metrics
    fallback.py             # Fallback strategies + circuit breaker
  data/
    validators.py           # Input validation utilities
    preprocessors.py        # Text, image, tabular preprocessing
  monitoring/
    metrics.py              # Latency, error rate, p95/p99 tracking
    logger.py               # Structured logging setup
  api/routes/
    predict.py              # POST /api/predict, GET /api/health, GET /api/metrics
```

## Setup

```bash
cd projects/05-production-ai-system
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pydantic-settings
```

## Environment Variables

```env
ENVIRONMENT=development          # development | staging | production
MODEL_NAME=gpt-4
MODEL_VERSION=1.0
MAX_BATCH_SIZE=32
INFERENCE_TIMEOUT=30.0
ENABLE_FALLBACK=true
FALLBACK_MODEL=gpt-3.5-turbo
MAX_RETRIES=3
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-...
```

## Run

```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Run inference |
| GET | `/api/health` | Health check with model status |
| GET | `/api/metrics` | Request metrics (latency, errors) |
| GET | `/health` | Basic health check |

## Production Concerns This Scaffold Addresses

### 1. Input Validation & Sanitization
- Schema validation with Pydantic
- Length limits, type checking, batch size limits
- Output sanitization (PII, injection prevention)

### 2. Error Handling
- Typed exception hierarchy (ValidationError, ModelNotFoundError, InferenceError)
- Structured error responses with codes
- Unhandled exception catching

### 3. Model Management
- Load/unload models at startup
- Track model metadata and request counts
- Model versioning support (TODO)

### 4. Inference Pipeline
- Orchestrated flow: validate -> preprocess -> predict -> postprocess
- Each step is pluggable and replaceable
- Batch inference support (TODO)

### 5. Fallback & Resilience
- Retry with exponential backoff
- Fallback to simpler model
- Circuit breaker pattern (TODO)
- Graceful degradation

### 6. Monitoring & Observability
- Request timing headers (X-Process-Time-Ms)
- Request tracing (X-Request-ID)
- Latency metrics (avg, p95, p99)
- Error rate tracking
- Structured JSON logging (TODO)

### 7. Health Checks
- Liveness check (is the service running?)
- Readiness check (are models loaded?)
- Model status reporting

## Integrating Real Models

### HuggingFace Transformers
```python
# In model_manager.py load_model():
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
```

### ONNX Runtime
```python
import onnxruntime as ort

session = ort.InferenceSession("model.onnx")
outputs = session.run(None, {"input": input_array})
```

### OpenAI API
```python
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": text}],
)
```

## Adding New Preprocessors

```python
from app.data.preprocessors import TextPreprocessor


class MyPreprocessor(TextPreprocessor):
    def preprocess(self, text: str) -> dict:
        # Your custom preprocessing
        tokens = my_tokenizer(text)
        return {"tokens": tokens}
```

## Adding New Evaluation Metrics

```python
from app.ai.evaluation import EvaluationMetrics


# Add custom metrics
def custom_metric(predictions, labels):
    # Your metric logic
    return score
```
