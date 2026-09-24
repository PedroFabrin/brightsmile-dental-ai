import re
from pathlib import Path

from app.rag.models import Chunk

FAQ_FILE = "faq.md"


def _split_sections(markdown: str, level: int) -> tuple[str, list[tuple[str, str]]]:
    """Return the H1 title and the (heading, body) pairs for headings of the given level."""
    title_match = re.search(r"^# (.+)$", markdown, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""
    marker = "#" * level
    parts = re.split(rf"^{marker} (.+)$", markdown, flags=re.MULTILINE)
    # parts = [preamble, heading1, body1, heading2, body2, ...]
    sections = [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts) - 1, 2)]
    return title, sections


def chunk_document(path: Path) -> list[Chunk]:
    """Split one Markdown file into chunks.

    `faq.md`: one chunk per question/answer (### headings).
    Other files: one chunk per section (## headings), keeping the section title.
    """
    markdown = path.read_text(encoding="utf-8")
    level = 3 if path.name == FAQ_FILE else 2
    title, sections = _split_sections(markdown, level)
    chunks = []
    for index, (heading, body) in enumerate(sections):
        if not body:
            continue
        chunks.append(
            Chunk(
                id=f"{path.stem}-{index}",
                text=f"{title} - {heading}\n{body}",
                source=path.name,
                doc_title=title,
                section=heading,
            )
        )
    return chunks


def load_chunks(data_dir: Path) -> list[Chunk]:
    """Chunk every Markdown file in `data_dir`."""
    chunks: list[Chunk] = []
    for path in sorted(data_dir.glob("*.md")):
        chunks.extend(chunk_document(path))
    return chunks
