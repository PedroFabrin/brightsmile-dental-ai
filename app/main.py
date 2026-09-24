from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api import chat, health
from app.config import get_settings
from app.rag.service import ensure_index
from app.rate_limit import limiter


@asynccontextmanager
async def lifespan(_: FastAPI):
    if get_settings().auto_ingest:
        ensure_index()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="BrightSmile Dental AI Assistant", lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(chat.router)
    return app


app = create_app()
