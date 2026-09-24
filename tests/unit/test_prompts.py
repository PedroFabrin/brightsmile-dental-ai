from app.agent.prompts import NO_CONTEXT, SYSTEM_PROMPT, build_user_message
from app.rag.models import Chunk, RetrievedChunk


def test_user_message_wraps_context_and_question_as_data():
    chunk = RetrievedChunk(Chunk("a", "cleaning $110", "services.md", "Services", "Exams"), 0.9)
    message = build_user_message("How much is a cleaning?", [chunk])
    assert "[Source: services.md]" in message
    assert "<user_message>\nHow much is a cleaning?\n</user_message>" in message


def test_empty_context_is_marked():
    assert NO_CONTEXT in build_user_message("anything", [])


def test_system_prompt_has_the_mandatory_rules():
    for expected in ("ONLY", "human team member", "Source", "diagnosis", "DATA", "Portuguese"):
        assert expected in SYSTEM_PROMPT
