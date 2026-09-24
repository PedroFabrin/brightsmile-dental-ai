import chromadb
from chromadb.config import Settings as ChromaSettings

from app.rag.models import Chunk, RetrievedChunk
from app.rag.stores.base import VectorStore

COLLECTION = "brightsmile_kb"


class ChromaStore(VectorStore):
    """Chroma collection using cosine distance."""

    def __init__(self, path: str):
        self._client = chromadb.PersistentClient(
            path=path, settings=ChromaSettings(anonymized_telemetry=False)
        )
        self._collection = self._get_collection()

    def _get_collection(self):
        return self._client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    def reset(self) -> None:
        self._client.delete_collection(COLLECTION)
        self._collection = self._get_collection()

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self._collection.add(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=embeddings,
            metadatas=[
                {"source": c.source, "doc_title": c.doc_title, "section": c.section} for c in chunks
            ],
        )

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        total = self.count()
        if total == 0:
            return []
        result = self._collection.query(query_embeddings=[embedding], n_results=min(top_k, total))
        retrieved = []
        for chunk_id, text, meta, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        ):
            chunk = Chunk(
                id=chunk_id,
                text=text,
                source=meta["source"],
                doc_title=meta["doc_title"],
                section=meta["section"],
            )
            retrieved.append(RetrievedChunk(chunk=chunk, score=1.0 - distance))
        return retrieved

    def count(self) -> int:
        return self._collection.count()
