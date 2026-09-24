from pathlib import Path

from app.rag.chunking import chunk_document, load_chunks

DATA_DIR = Path(__file__).parents[2] / "data"


def test_regular_document_splits_by_section_and_keeps_title(tmp_path):
    doc = tmp_path / "services.md"
    doc.write_text("# Services\n\nintro\n\n## Exams\n- a: $1\n\n## Cosmetic\n- b: $2\n")
    chunks = chunk_document(doc)
    assert [c.section for c in chunks] == ["Exams", "Cosmetic"]
    assert chunks[0].source == "services.md"
    assert chunks[0].doc_title == "Services"
    assert "a: $1" in chunks[0].text
    assert "b: $2" not in chunks[0].text


def test_faq_makes_one_chunk_per_question(tmp_path):
    doc = tmp_path / "faq.md"
    doc.write_text("# FAQ\n\n### Q one?\n\nAnswer one.\n\n### Q two?\n\nAnswer two.\n")
    chunks = chunk_document(doc)
    assert [c.section for c in chunks] == ["Q one?", "Q two?"]
    assert "Answer one." in chunks[0].text


def test_chunk_ids_are_unique_across_the_real_knowledge_base():
    chunks = load_chunks(DATA_DIR)
    assert len({c.id for c in chunks}) == len(chunks)
    assert {c.source for c in chunks} == {
        f"{name}.md"
        for name in ("about", "services", "hours", "insurance", "policies", "team", "faq")
    }


def test_faq_has_between_15_and_20_questions():
    faq_chunks = [c for c in load_chunks(DATA_DIR) if c.source == "faq.md"]
    assert 15 <= len(faq_chunks) <= 20
