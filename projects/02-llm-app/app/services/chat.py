import re
from collections.abc import AsyncIterator

from app.core.exceptions import LLMServiceError
from app.llm.base import LLMProvider
from app.llm.factory import get_llm_provider
from app.schemas.llm import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ClassifyRequest,
    ClassifyResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from app.services.prompt_templates import PROMPT_TEMPLATES


class ChatService:
    """Service for LLM-powered chat, summarization, and classification."""

    def __init__(self, provider: LLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Handle a chat completion request."""
        try:
            return await self._provider.generate(
                messages=request.messages,
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(message=f"Chat generation failed: {e}") from e

    async def chat_stream(self, request: ChatRequest) -> AsyncIterator[str]:
        """Handle a streaming chat completion request."""
        try:
            async for chunk in self._provider.generate_stream(
                messages=request.messages,
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            ):
                yield chunk
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(message=f"Stream generation failed: {e}") from e

    async def summarize(self, request: SummarizeRequest) -> SummarizeResponse:
        """Summarize the provided text."""
        template = PROMPT_TEMPLATES["summarize"]
        prompt = template.format(text=request.text, max_length=request.max_length)

        messages = [ChatMessage(role="user", content=prompt)]

        try:
            response = await self._provider.generate(
                messages=messages,
                model=request.model,
            )
            return SummarizeResponse(
                summary=response.content,
                model=response.model,
                usage=response.usage,
            )
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(message=f"Summarization failed: {e}") from e

    async def classify(self, request: ClassifyRequest) -> ClassifyResponse:
        """Classify text into one of the provided categories."""
        categories_str = ", ".join(request.categories)
        template = PROMPT_TEMPLATES["classify"]
        prompt = template.format(text=request.text, categories=categories_str)

        messages = [ChatMessage(role="user", content=prompt)]

        try:
            response = await self._provider.generate(
                messages=messages,
                model=request.model,
            )

            category, confidence = self._parse_classification(
                response.content, request.categories
            )

            return ClassifyResponse(
                category=category,
                confidence=confidence,
                model=response.model,
                usage=response.usage,
            )
        except LLMServiceError:
            raise
        except Exception as e:
            raise LLMServiceError(message=f"Classification failed: {e}") from e

    def _parse_classification(
        self, response_text: str, valid_categories: list[str]
    ) -> tuple[str, float]:
        """Parse the classification response to extract category and confidence."""
        category_match = re.search(r"Category:\s*(.+)", response_text, re.IGNORECASE)
        confidence_match = re.search(
            r"Confidence:\s*([\d.]+)", response_text, re.IGNORECASE
        )

        category = category_match.group(1).strip() if category_match else ""
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5

        if category.lower() not in [c.lower() for c in valid_categories]:
            for c in valid_categories:
                if c.lower() in response_text.lower():
                    category = c
                    break
            else:
                category = valid_categories[0]

        confidence = max(0.0, min(1.0, confidence))

        return category, confidence
