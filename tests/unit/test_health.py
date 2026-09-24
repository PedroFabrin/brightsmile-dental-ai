from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_configured_origin_only():
    allowed = client.get("/health", headers={"Origin": "http://localhost:8000"})
    denied = client.get("/health", headers={"Origin": "http://evil.example"})
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:8000"
    assert "access-control-allow-origin" not in denied.headers
