from dataclasses import dataclass

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import SYSTEM_PROMPT, build_user_message
from app.rag.models import RetrievedChunk
from app.rag.retriever import Retriever


@dataclass(frozen=True)
class Source:
    source: str
    section: str


@dataclass(frozen=True)
class ChatAnswer:
    answer: str
    sources: list[Source]


class ChatService:
    """Phase 2 chat flow: retrieve context, then ask the LLM. The agent replaces it in Phase 3."""

    def __init__(self, retriever: Retriever, model: BaseChatModel):
        self._retriever = retriever
        self._model = model

    def answer(self, question: str) -> ChatAnswer:
        chunks = self._retriever.retrieve(question)
        response = self._model.invoke(
            [SystemMessage(SYSTEM_PROMPT), HumanMessage(build_user_message(question, chunks))]
        )
        answer = response.text.strip()
        return ChatAnswer(answer=answer, sources=self._cited_sources(answer, chunks))

    @staticmethod
    def _cited_sources(answer: str, chunks: list[RetrievedChunk]) -> list[Source]:
        """Sources of the retrieved chunks whose document the answer cites, e.g. "services.md"."""
        cited = (r.chunk for r in chunks if r.chunk.source in answer)
        return list(dict.fromkeys(Source(c.source, c.section) for c in cited))
