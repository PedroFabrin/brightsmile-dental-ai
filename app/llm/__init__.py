from app.config import Settings
from app.llm.base import LLMProvider, MissingApiKeyError
from app.llm.providers import AnthropicProvider, GeminiProvider, OpenAIProvider

__all__ = [
    "AnthropicProvider",
    "GeminiProvider",
    "LLMProvider",
    "MissingApiKeyError",
    "OpenAIProvider",
    "get_llm_provider",
]


def get_llm_provider(settings: Settings) -> LLMProvider:
    """Build the provider selected by `LLM_PROVIDER`."""
    if settings.llm_provider == "gemini":
        return GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    if settings.llm_provider == "anthropic":
        return AnthropicProvider(settings.anthropic_api_key)
    return OpenAIProvider(settings.openai_api_key)
