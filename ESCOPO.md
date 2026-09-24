# Scope — BrightSmile Dental AI Assistant

## Original request

> Demo pública de agente de atendimento com IA para uma clínica odontológica fictícia (BrightSmile Dental), com RAG, ferramentas de agendamento, widget de chat, testes de avaliação e deploy no Fly.io. Objetivo: vitrine no GitHub, no Fiverr e nas redes.

Portfolio project (no external client). The reference document is `CLAUDE.md`.

> Update after Phase 1: hosting moved from Fly.io (mentioned in the original request above) to Hugging Face Spaces, and the default LLM to Gemini free tier, to keep the project at zero cost.

## Understanding

- Public AI customer-service agent for a fictional dental clinic.
- RAG over a Markdown knowledge base (`data/`), answers cite their source document.
- Tools: `check_availability`, `request_appointment`, `handoff_to_human`.
- FastAPI API with SSE streaming; embeddable chat widget plus a chat page (plain HTML/CSS/JS).
- Pluggable LLM (Gemini default, Anthropic, OpenAI) and vector store (Chroma/Pinecone) via `.env`.
- Evaluation suite (25+ cases, real LLM, outside the default test run) with a hit-rate report.
- Deploy on Hugging Face Spaces (Docker, free CPU), with rate limiting and graceful handling of LLM usage limits.
- Zero cost: default LLM is Gemini free tier.
- Showcase: GitHub, Fiverr, LinkedIn/Instagram.

## Open questions

- Gemini free-tier quota is small: is a 429 message ("usage limit reached") acceptable for the public demo? (assumed: yes)
- Hugging Face account and Space name?
- Is `check_availability` backed by fake static slots, or a generated schedule? (assumed: fake slots)
- Public repo name and GitHub account?

## Out of scope

- Real clinic data, real patients or real bookings (no real integrations, calendars, e-mail/SMS sending).
- Medical advice or diagnosis by the bot.
- Authentication for end users, admin UI, or a build-step frontend framework.
- Dependencies outside the stack listed in `CLAUDE.md` (ask first).
- Deploying or pushing to a public repository without Pedro's explicit approval.
