import pytest

from app.rag.embeddings import Embedder
from app.rag.models import Chunk
from app.rag.retriever import Retriever
from app.rag.stores.base import VectorStore
from app.rag.stores.chroma_store import ChromaStore


class FakeEmbedder(Embedder):
    """Maps a keyword to a fixed 3D vector so similarity is predictable."""

    VECTORS = {"price": [1.0, 0.0, 0.0], "hours": [0.0, 1.0, 0.0], "other": [0.0, 0.0, 1.0]}

    def embed(self, texts):
        return [next((v for k, v in self.VECTORS.items() if k in t), [1, 1, 1]) for t in texts]


def make_chunk(chunk_id, source, section="S"):
    return Chunk(chunk_id, f"text {chunk_id}", source, "Title", section)


@pytest.fixture
def store(tmp_path) -> VectorStore:
    store = ChromaStore(str(tmp_path / "chroma"))
    chunks = [make_chunk("a", "services.md", "Prices"), make_chunk("b", "hours.md", "Regular")]
    store.add(chunks, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    return store


def test_chroma_store_returns_best_match_first_with_cosine_score(store):
    results = store.query([1.0, 0.0, 0.0], top_k=2)
    assert [r.chunk.id for r in results] == ["a", "b"]
    assert results[0].score == pytest.approx(1.0)
    assert results[1].score == pytest.approx(0.0, abs=1e-6)
    assert results[0].chunk.source == "services.md"
    assert results[0].chunk.section == "Prices"


def test_chroma_store_reset_and_count(store):
    assert store.count() == 2
    store.reset()
    assert store.count() == 0
    assert store.query([1.0, 0.0, 0.0], top_k=3) == []


def test_retriever_returns_relevant_chunks_with_sources(store):
    retriever = Retriever(FakeEmbedder(), store, top_k=2, min_score=0.5)
    results = retriever.retrieve("price?")
    assert [r.chunk.source for r in results] == ["services.md"]


def test_retriever_returns_nothing_below_min_score(store):
    retriever = Retriever(FakeEmbedder(), store, top_k=2, min_score=0.5)
    assert retriever.retrieve("other") == []


def test_retriever_respects_top_k(store):
    retriever = Retriever(FakeEmbedder(), store, top_k=1, min_score=0.0)
    assert len(retriever.retrieve("unknown words")) == 1
