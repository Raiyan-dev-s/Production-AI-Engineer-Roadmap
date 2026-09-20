# AI Application Architecture

## Overview

How to structure AI applications for reliability, maintainability, and scale.

## Separation of Concerns

```
app/
├── api/              # HTTP endpoints (FastAPI routers)
│   ├── routes/
│   └── dependencies/
├── core/             # Business logic, config
│   ├── config.py
│   └── exceptions.py
├── models/           # Pydantic models, DB models
│   ├── schemas.py
│   └── database.py
├── services/         # Business logic
│   ├── llm.py        # LLM client wrapper
│   ├── rag.py        # RAG pipeline
│   └── auth.py       # Authentication
└── main.py           # App entry point
```

**Key rule**: keep AI logic in services, not in routes.

## LLM Integration Patterns

### Pattern 1: Direct API Calls

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def generate_response(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

Best for: simple use cases, full control.

### Pattern 2: Provider Abstraction

```python
from litellm import acompletion


async def generate_response(prompt: str, model: str = "gpt-4o") -> str:
    response = await acompletion(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

Best for: flexibility to switch providers.

### Pattern 3: Structured Output

```python
from pydantic import BaseModel


class SentimentResult(BaseModel):
    sentiment: str
    confidence: float
    reasoning: str


async def analyze_sentiment(text: str) -> SentimentResult:
    response = await client.chat.completions.create(
        model="gpt-4o", messages=[...], response_format={"type": "json_object"}
    )
    return SentimentResult.model_validate_json(response.choices[0].message.content)
```

Best for: when you need typed, validated output.

## RAG Integration

```python
class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    async def answer(self, question: str) -> str:
        # Retrieve relevant chunks
        chunks = await self.vector_store.similarity_search(question, k=5)

        # Build context
        context = "\n\n".join([c.text for c in chunks])

        # Generate answer
        prompt = f"""Answer the question based on the context.

Context: {context}

Question: {question}

Answer:"""

        return await self.llm.generate(prompt)
```

## Agent Integration

```python
class Agent:
    def __init__(self, tools: list[Tool], llm):
        self.tools = {t.name: t for t in tools}
        self.llm = llm

    async def run(self, goal: str) -> str:
        messages = [{"role": "user", "content": goal}]

        while True:
            response = await self.llm.chat(
                messages=messages, tools=[t.definition for t in self.tools.values()]
            )

            if not response.tool_calls:
                return response.content

            for tool_call in response.tool_calls:
                tool = self.tools[tool_call.function.name]
                result = await tool.execute(**tool_call.function.arguments)
                messages.append({"role": "tool", "content": result})
```

## Evaluation

### Build Evaluation Datasets

```python
eval_dataset = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe...",
    },
    # ... more examples
]
```

### Run Evaluations

```python
async def evaluate(rag_service, dataset):
    results = []
    for item in dataset:
        response = await rag_service.answer(item["input"])
        results.append(
            {
                "correct": response == item["expected"],
                "input": item["input"],
                "expected": item["expected"],
                "got": response,
            }
        )
    accuracy = sum(r["correct"] for r in results) / len(results)
    return {"accuracy": accuracy, "details": results}
```

## Key Principles

1. **Don't put AI logic in routes** — keep it in services
2. **Abstract LLM providers** — make it easy to switch
3. **Use Pydantic for structured output** — validate everything
4. **Build evaluation sets early** — you can't improve what you can't measure
5. **Design for failure** — LLM calls fail, handle it gracefully
6. **Cache aggressively** — embeddings, completions, retrieval results
7. **Log everything** — you'll need it for debugging and evaluation
