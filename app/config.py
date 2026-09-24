from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables / `.env`."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    cors_origins: list[str] = ["http://localhost:7860"]
    rate_limit_per_minute: int = 20
    max_tokens_per_response: int = 500
    history_max_messages: int = 10
    admin_api_key: str = ""

    llm_provider: Literal["gemini", "anthropic", "openai"] = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash"
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    data_dir: str = "data"
    storage_dir: str = "storage"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_cache_dir: str = "models"
    vector_store: Literal["chroma"] = "chroma"
    auto_ingest: bool = True
    retrieval_top_k: int = 4
    retrieval_min_score: float = 0.30  # cosine similarity, to be calibrated with the eval (Phase 4)
    max_message_chars: int = 1000
    trust_proxy_headers: bool = False  # read the client IP from X-Forwarded-For (behind a proxy)


@lru_cache
def get_settings() -> Settings:
    return Settings()
