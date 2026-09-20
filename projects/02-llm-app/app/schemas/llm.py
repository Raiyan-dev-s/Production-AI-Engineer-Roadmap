from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class TokenUsage(BaseModel):
    prompt_tokens: int = Field(default=0, description="Number of prompt tokens")
    completion_tokens: int = Field(default=0, description="Number of completion tokens")
    total_tokens: int = Field(default=0, description="Total tokens used")


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(
        ..., min_length=1, description="List of chat messages"
    )
    model: str | None = Field(default=None, description="Model override")
    max_tokens: int | None = Field(default=None, description="Max tokens override")
    temperature: float | None = Field(default=None, description="Temperature override")
    stream: bool = Field(default=False, description="Enable streaming response")


class ChatResponse(BaseModel):
    content: str = Field(..., description="Generated response content")
    model: str = Field(..., description="Model used for generation")
    usage: TokenUsage = Field(
        default_factory=TokenUsage, description="Token usage info"
    )


class ModelInfo(BaseModel):
    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Human-readable model name")
    provider: str = Field(..., description="Provider name")
    max_tokens: int = Field(default=4096, description="Maximum context tokens")


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    max_length: int = Field(default=150, description="Maximum summary length in words")
    model: str | None = Field(default=None, description="Model override")


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="Generated summary")
    model: str = Field(..., description="Model used")
    usage: TokenUsage = Field(
        default_factory=TokenUsage, description="Token usage info"
    )


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to classify")
    categories: list[str] = Field(..., min_length=1, description="Possible categories")
    model: str | None = Field(default=None, description="Model override")


class ClassifyResponse(BaseModel):
    category: str = Field(..., description="Assigned category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    model: str = Field(..., description="Model used")
    usage: TokenUsage = Field(
        default_factory=TokenUsage, description="Token usage info"
    )
