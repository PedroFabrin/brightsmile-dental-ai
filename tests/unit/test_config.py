from app.config import Settings


def test_defaults():
    settings = Settings(_env_file=None)
    assert settings.rate_limit_per_minute == 20
    assert settings.history_max_messages == 10


def test_reads_environment(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "5")
    monkeypatch.setenv("CORS_ORIGINS", '["https://example.com"]')
    settings = Settings(_env_file=None)
    assert settings.rate_limit_per_minute == 5
    assert settings.cors_origins == ["https://example.com"]
