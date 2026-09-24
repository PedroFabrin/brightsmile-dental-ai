from app.rag.embeddings import Embedder
from app.rag.models import RetrievedChunk
from app.rag.stores.base import VectorStore


class Retriever:
    """Finds the knowledge-base chunks relevant to a question, with their sources."""

    def __init__(self, embedder: Embedder, store: VectorStore, top_k: int, min_score: float):
        self._embedder = embedder
        self._store = store
        self._top_k = top_k
        self._min_score = min_score

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        embedding = self._embedder.embed([query])[0]
        results = self._store.query(embedding, self._top_k)
        return [r for r in results if r.score >= self._min_score]
