from abc import ABC, abstractmethod

from app.rag.models import Chunk, RetrievedChunk


class VectorStore(ABC):
    """Pluggable vector store. Switching stores is only a `.env` change."""

    @abstractmethod
    def reset(self) -> None:
        """Remove every stored chunk."""

    @abstractmethod
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Store chunks with their embeddings."""

    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        """Return the `top_k` most similar chunks, best first (score = cosine similarity)."""

    @abstractmethod
    def count(self) -> int:
        """Number of stored chunks."""
