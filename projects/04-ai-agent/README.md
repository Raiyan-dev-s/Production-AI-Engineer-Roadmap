# Project 04: AI Agent

A scaffold ReAct-style AI agent with a modular tool system and placeholder LLM reasoning.

## Agent Loop (ReAct)

```
  User Query
      |
      v
  +--------+     +--------+     +--------+     +--------+
  | THINK  | --> | DECIDE | --> |  ACT   | --> |OBSERVE |
  | reason |     | use    |     | execute|     | get    |
  | about  |     | tool?  |     | tool   |     | result |
  | problem|     | or     |     |        |     |        |
  |        |     | answer?|     |        |     |        |
  +--------+     +--------+     +--------+     +--------+
      ^                                              |
      |            (if tool was used)                |
      +----------------------------------------------+

  When decision is "answer" -> return final response
```

## Architecture

```
app/
  main.py                   # FastAPI entry point
  core/
    config.py               # Settings (LLM, agent limits)
  schemas/
    agent.py                # AgentRequest/Response, ToolCall, ToolResult
  agent/
    base.py                 # BaseAgent abstract class
    react_agent.py          # ReAct agent (reason + act loop)
    orchestrator.py         # Agent lifecycle management
  tools/
    base.py                 # BaseTool abstract class
    calculator.py           # Real math expression evaluator (AST-based)
    search.py               # Web search (placeholder)
    database.py             # DB lookup (placeholder)
    registry.py             # Tool registration and lookup
  api/routes/
    agent.py                # POST /api/agent/run, GET /api/agent/tools
```

## Setup

```bash
cd projects/04-ai-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pydantic-settings
```

## Environment Variables

```env
LLM_PROVIDER=mock            # mock | openai
LLM_MODEL=gpt-4
MAX_ITERATIONS=10
MAX_TOOL_CALLS=5
OPENAI_API_KEY=sk-...
```

## Run

```bash
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/agent/run` | Run the agent on a query |
| GET | `/api/agent/tools` | List available tools |
| GET | `/health` | Health check |

## Tool System

### Built-in Tools

| Tool | Description | Status |
|------|-------------|--------|
| `calculator` | Evaluates math expressions | Working |
| `search` | Web search | Placeholder (mock results) |
| `database_lookup` | Database queries | Placeholder (mock data) |

### Adding a New Tool

1. Create a new file in `app/tools/`:

```python
from app.tools.base import BaseTool


class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "weather"

    @property
    def description(self) -> str:
        return "Gets current weather for a city. Input: city name string."

    def execute(self, city: str = "", **kwargs) -> dict:
        # Real implementation here
        return {"city": city, "temp": 72, "condition": "sunny"}
```

2. Register it in `app/agent/orchestrator.py`:

```python
from app.tools.weather import WeatherTool


def _register_default_tools(self):
    # ... existing tools ...
    self.tool_registry.register(WeatherTool())
```

### Tool Design Principles

- **Clear description**: The agent reads tool descriptions to decide when to use them
- **Specific inputs**: Document what arguments the tool expects
- **Error handling**: Raise clear errors; the agent sees them as observations
- **Single responsibility**: Each tool does one thing well

## Integrating Real LLM Reasoning

Replace the mock `think()` and `decide()` methods in `react_agent.py` with real LLM calls:

```python
def think(self, request, history):
    messages = [
        {"role": "system", "content": REACT_PROMPT},
        {"role": "user", "content": request.query},
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
    return response.choices[0].message.content


def decide(self, thought, available_tools):
    # Parse LLM output for "Action: tool_name(args)" or "Final Answer: ..."
    # Return ToolCall or final answer string
    ...
```

## Extending the Agent

- **Add memory**: Store conversation history across runs
- **Add planning**: Pre-compute a plan before executing
- **Add reflection**: Agent reviews its own output for quality
- **Multi-agent**: Orchestrator coordinates multiple specialized agents
