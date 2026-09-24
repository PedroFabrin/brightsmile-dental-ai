from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """A piece of the knowledge base, with the document it came from."""

    id: str
    text: str
    source: str  # file name, e.g. "services.md"
    doc_title: str  # document title (H1)
    section: str  # section title (H2 / FAQ question)


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float  # cosine similarity, higher is better
