from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    call_id: str | None = None


class ToolResult(BaseModel):
    tool_name: str
    call_id: str | None = None
    result: Any = None
    error: str | None = None
    success: bool = True


class AgentRequest(BaseModel):
    query: str
    context: dict[str, Any] | None = None
    max_iterations: int = 10


class AgentStep(BaseModel):
    step_number: int
    thought: str = ""
    action: ToolCall | None = None
    observation: ToolResult | None = None


class AgentResponse(BaseModel):
    answer: str
    steps: list[AgentStep]
    tool_calls_made: int = 0
    iterations: int = 0
