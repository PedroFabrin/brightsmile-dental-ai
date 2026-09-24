import pytest

from app.config import Settings
from app.llm import (
    AnthropicProvider,
    GeminiProvider,
    LLMProvider,
    MissingApiKeyError,
    OpenAIProvider,
    get_llm_provider,
)


@pytest.mark.parametrize(
    ("provider", "expected"),
    [("gemini", GeminiProvider), ("anthropic", AnthropicProvider), ("openai", OpenAIProvider)],
)
def test_factory_selects_provider_from_settings(provider, expected):
    result = get_llm_provider(Settings(_env_file=None, llm_provider=provider))
    assert isinstance(result, expected)
    assert isinstance(result, LLMProvider)


def test_default_provider_is_gemini():
    assert Settings(_env_file=None).llm_provider == "gemini"


def test_missing_api_key_fails_with_clear_error():
    provider = get_llm_provider(Settings(_env_file=None, gemini_api_key=""))
    with pytest.raises(MissingApiKeyError, match="GEMINI_API_KEY"):
        provider.get_chat_model(max_tokens=100)


def test_gemini_builds_chat_model_with_token_limit():
    provider = GeminiProvider(api_key="fake-key", model="gemini-3.5-flash")
    model = provider.get_chat_model(max_tokens=123)
    assert model.max_output_tokens == 123
    assert model.model.endswith("gemini-3.5-flash")


def test_llm_provider_is_abstract():
    with pytest.raises(TypeError):
        LLMProvider()  # type: ignore[abstract]
