import logging
from functools import lru_cache
from pathlib import Path

from app.config import Settings, get_settings
from app.rag.chunking import load_chunks
from app.rag.embeddings import Embedder, FastEmbedder
from app.rag.retriever import Retriever
from app.rag.stores.base import VectorStore
from app.rag.stores.chroma_store import ChromaStore

logger = logging.getLogger(__name__)


def build_embedder(settings: Settings) -> Embedder:
    return FastEmbedder(settings.embedding_model, settings.embedding_cache_dir)


def build_store(settings: Settings) -> VectorStore:
    """Build the vector store selected by `VECTOR_STORE`."""
    return ChromaStore(str(Path(settings.storage_dir) / "chroma"))


@lru_cache
def get_embedder() -> Embedder:
    return build_embedder(get_settings())


@lru_cache
def get_store() -> VectorStore:
    return build_store(get_settings())


@lru_cache
def get_retriever() -> Retriever:
    settings = get_settings()
    return Retriever(
        get_embedder(),
        get_store(),
        top_k=settings.retrieval_top_k,
        min_score=settings.retrieval_min_score,
    )


def ingest(data_dir: Path, embedder: Embedder, store: VectorStore) -> int:
    """Rebuild the index from scratch. Returns the number of chunks stored."""
    chunks = load_chunks(data_dir)
    embeddings = embedder.embed([c.text for c in chunks])
    store.reset()
    store.add(chunks, embeddings)
    logger.info("Indexed %d chunks from %s", len(chunks), data_dir)
    return len(chunks)


def ensure_index() -> None:
    """Index the knowledge base if the store is empty (the free Space disk is ephemeral)."""
    store = get_store()
    if store.count() == 0:
        ingest(Path(get_settings().data_dir), get_embedder(), store)
