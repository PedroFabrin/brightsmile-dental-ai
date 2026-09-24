from fastapi.testclient import TestClient
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from app.api.chat import get_chat_service
from app.config import get_settings
from app.main import app
from app.rag.models import Chunk, RetrievedChunk
from app.services.chat import ChatService


class FakeRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.queries = []

    def retrieve(self, query):
        self.queries.append(query)
        return self.chunks


def make_service(chunks, reply="Whitening costs $350. (Source: services.md)"):
    model = FakeListChatModel(responses=[reply])
    return ChatService(FakeRetriever(chunks), model)


CHUNK = RetrievedChunk(
    Chunk("services-2", "whitening $350", "services.md", "Services", "Cosmetic"), 0.8
)


def client_with(service):
    app.dependency_overrides[get_chat_service] = lambda: service
    return TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_chat_returns_answer_with_sources():
    response = client_with(make_service([CHUNK])).post("/chat", json={"message": "whitening?"})
    assert response.status_code == 200
    body = response.json()
    assert "$350" in body["answer"]
    assert body["sources"] == [{"source": "services.md", "section": "Cosmetic"}]


def test_chat_without_context_returns_no_sources():
    response = client_with(make_service([], "I don't know.")).post("/chat", json={"message": "hi"})
    assert response.json()["sources"] == []


def test_chat_rejects_empty_and_too_long_messages():
    client = client_with(make_service([]))
    assert client.post("/chat", json={"message": ""}).status_code == 422
    too_long = "x" * (get_settings().max_message_chars + 1)
    assert client.post("/chat", json={"message": too_long}).status_code == 422


def test_chat_is_rate_limited_per_ip(monkeypatch):
    from app.rate_limit import limiter

    monkeypatch.setattr(get_settings(), "rate_limit_per_minute", 2)
    limiter.reset()
    client = client_with(make_service([], "ok"))
    statuses = [client.post("/chat", json={"message": "hi"}).status_code for _ in range(3)]
    limiter.reset()
    assert statuses == [200, 200, 429]


def test_chat_lists_only_sources_cited_in_the_answer():
    other = RetrievedChunk(Chunk("hours-0", "open 8am", "hours.md", "Hours", "Regular"), 0.7)
    response = client_with(make_service([CHUNK, other])).post(
        "/chat", json={"message": "whitening?"}
    )
    assert [s["source"] for s in response.json()["sources"]] == ["services.md"]
