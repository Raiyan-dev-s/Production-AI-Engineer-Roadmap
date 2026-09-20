import asyncio
import random
from collections.abc import AsyncIterator

from app.llm.base import LLMProvider
from app.schemas.llm import ChatMessage, ChatResponse, ModelInfo, TokenUsage

MOCK_RESPONSES: dict[str, list[str] | dict[str, list[str]]] = {
    "default": [
        "I understand your question. Here's a detailed response based on my analysis of the provided context. The key points are: first, the information suggests a strong correlation between the variables mentioned. Second, there are several factors to consider when interpreting these results. Would you like me to elaborate on any specific aspect?",
        "Based on my analysis, here are the key findings: The data indicates a clear trend that supports the hypothesis. However, there are some edge cases worth noting. I'd recommend considering these additional factors before drawing final conclusions.",
        "That's an interesting question. Let me break this down into components: The primary factor is the relationship between input and output quality. Secondary considerations include scalability and resource constraints. I can provide more detail on any of these points.",
    ],
    "summarize": [
        "The provided text discusses several interconnected themes. The main argument centers on the relationship between technology and human behavior, supported by empirical evidence from multiple studies. Key conclusions include the need for balanced approaches to implementation and ongoing evaluation of outcomes.",
        "This passage presents a comprehensive overview of the topic. The central thesis argues for a nuanced understanding of the subject matter, acknowledging both benefits and potential drawbacks. The author supports this position with concrete examples and statistical data.",
    ],
    "classify": {
        "positive": [
            "This content expresses enthusiasm, approval, and optimistic sentiment throughout. The language is constructive and forward-looking.",
        ],
        "negative": [
            "This content expresses criticism, concerns, and cautious sentiment. The language suggests areas for improvement and potential risks.",
        ],
        "neutral": [
            "This content presents information in a balanced, factual manner without strong emotional indicators. The tone is objective and analytical.",
        ],
    },
}

MOCK_MODELS = [
    ModelInfo(id="mock-7b", name="Mock 7B", provider="mock", max_tokens=4096),
    ModelInfo(id="mock-13b", name="Mock 13B", provider="mock", max_tokens=8192),
    ModelInfo(id="mock-70b", name="Mock 70B", provider="mock", max_tokens=32768),
]


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for development and testing."""

    def __init__(self) -> None:
        self._default_model = "mock-7b"

    async def generate(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ChatResponse:
        target_model = model or self._default_model
        latency = random.uniform(0.1, 0.5)
        await asyncio.sleep(latency)

        last_message = messages[-1].content.lower() if messages else ""
        content = self._select_response(last_message)

        prompt_tokens = sum(len(m.content.split()) * 1.3 for m in messages)
        completion_tokens = len(content.split()) * 1.3

        return ChatResponse(
            content=content,
            model=target_model,
            usage=TokenUsage(
                prompt_tokens=int(prompt_tokens),
                completion_tokens=int(completion_tokens),
                total_tokens=int(prompt_tokens + completion_tokens),
            ),
        )

    async def generate_stream(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> AsyncIterator[str]:
        last_message = messages[-1].content.lower() if messages else ""
        content = self._select_response(last_message)
        words = content.split(" ")

        chunk_size = random.randint(2, 5)
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            if i + chunk_size < len(words):
                chunk += " "
            await asyncio.sleep(random.uniform(0.02, 0.08))
            yield chunk

    async def get_model_info(self, model: str | None = None) -> ModelInfo:
        target_model = model or self._default_model
        for m in MOCK_MODELS:
            if m.id == target_model:
                return m
        return MOCK_MODELS[0]

    async def list_models(self) -> list[ModelInfo]:
        return MOCK_MODELS.copy()

    def _select_response(self, prompt: str) -> str:
        if "summariz" in prompt or "summary" in prompt:
            responses = MOCK_RESPONSES["summarize"]
            assert isinstance(responses, list)
            return random.choice(responses)

        if "classif" in prompt or "categor" in prompt:
            category = random.choice(["positive", "negative", "neutral"])
            classify_responses = MOCK_RESPONSES["classify"]
            if isinstance(classify_responses, dict):
                return random.choice(classify_responses[category])
            return random.choice(classify_responses)

        default_responses = MOCK_RESPONSES["default"]
        assert isinstance(default_responses, list)
        return random.choice(default_responses)
