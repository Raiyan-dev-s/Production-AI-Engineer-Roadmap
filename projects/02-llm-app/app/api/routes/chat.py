from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.llm.factory import get_llm_provider
from app.schemas.llm import (
    ChatRequest,
    ChatResponse,
    ClassifyRequest,
    ClassifyResponse,
    ModelInfo,
    SummarizeRequest,
    SummarizeResponse,
)
from app.services.chat import ChatService

router = APIRouter(prefix="/api", tags=["llm"])


def _get_chat_service() -> ChatService:
    return ChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> Any:
    """Send a chat message and receive a completion."""
    service = _get_chat_service()
    if request.stream:
        import json

        async def event_stream() -> AsyncIterator[str]:
            async for chunk in service.chat_stream(request):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    return await service.chat(request)


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize the provided text."""
    service = _get_chat_service()
    return await service.summarize(request)


@router.post("/classify", response_model=ClassifyResponse)
async def classify(request: ClassifyRequest) -> ClassifyResponse:
    """Classify text into one of the provided categories."""
    service = _get_chat_service()
    return await service.classify(request)


@router.get("/models", response_model=list[ModelInfo])
async def list_models() -> list[ModelInfo]:
    """List all available models from the current provider."""
    provider = get_llm_provider()
    return await provider.list_models()
