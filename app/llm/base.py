from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel


class LLMProvider(ABC):
    """Pluggable LLM backend. Switching providers is only a `.env` change."""

    name: str

    @abstractmethod
    def get_chat_model(self, max_tokens: int) -> BaseChatModel:
        """Return a LangChain chat model limited to `max_tokens` output tokens."""


class MissingApiKeyError(RuntimeError):
    """Raised when the selected provider has no API key configured."""
