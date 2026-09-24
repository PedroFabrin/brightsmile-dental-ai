from langchain_core.language_models.chat_models import BaseChatModel

from app.llm.base import LLMProvider, MissingApiKeyError


def _require_key(provider: str, api_key: str) -> str:
    if not api_key:
        raise MissingApiKeyError(f"{provider.upper()}_API_KEY is not set")
    return api_key


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str):
        self._api_key = api_key
        self._model = model

    def get_chat_model(self, max_tokens: int) -> BaseChatModel:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=self._model,
            google_api_key=_require_key(self.name, self._api_key),
            max_output_tokens=max_tokens,
            max_retries=0,  # retries are handled by the agent (short backoff, max 2)
        )


class AnthropicProvider(LLMProvider):
    """Optional provider: requires `pip install langchain-anthropic`."""

    name = "anthropic"

    def __init__(self, api_key: str, model: str = "claude-haiku-4-5-20251001"):
        self._api_key = api_key
        self._model = model

    def get_chat_model(self, max_tokens: int) -> BaseChatModel:
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=self._model,
            api_key=_require_key(self.name, self._api_key),
            max_tokens=max_tokens,
            max_retries=0,
        )


class OpenAIProvider(LLMProvider):
    """Optional provider: requires `pip install langchain-openai`."""

    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self._api_key = api_key
        self._model = model

    def get_chat_model(self, max_tokens: int) -> BaseChatModel:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=self._model,
            api_key=_require_key(self.name, self._api_key),
            max_tokens=max_tokens,
            max_retries=0,
        )
