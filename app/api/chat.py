from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.config import get_settings
from app.llm import MissingApiKeyError, get_llm_provider
from app.rag.service import get_retriever
from app.rate_limit import chat_limit, limiter
from app.services.chat import ChatService

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=get_settings().max_message_chars)


class SourceOut(BaseModel):
    source: str
    section: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceOut]


@lru_cache
def get_chat_service() -> ChatService:
    settings = get_settings()
    provider = get_llm_provider(settings)
    try:
        model = provider.get_chat_model(settings.max_tokens_per_response)
    except MissingApiKeyError as error:
        raise HTTPException(
            status_code=503, detail="The assistant is not configured yet."
        ) from error
    return ChatService(get_retriever(), model)


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(chat_limit)
def chat(
    request: Request, body: ChatRequest, service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    result = service.answer(body.message)
    return ChatResponse(
        answer=result.answer,
        sources=[SourceOut(source=s.source, section=s.section) for s in result.sources],
    )
