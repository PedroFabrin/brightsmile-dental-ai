# BrightSmile Dental AI Assistant

AI customer-service agent demo for a fictional dental clinic (RAG, scheduling tools, chat widget, evals).

> Work in progress. Full README arrives in Phase 6.

## Free tier notes

- **Zero cost by default:** the LLM is Gemini on the Google AI Studio free tier, and the demo is hosted on
  Hugging Face Spaces (free CPU). On the free Gemini tier, Google may use conversation content to improve
  its products. That is acceptable here because the clinic and all data are fictional. For real use with
  customers, use a paid plan from any provider.
- **Temporary storage:** the free Space disk is wiped on restart, so conversation history and leads
  (SQLite) and the vector index are temporary. The index is rebuilt from `data/` at startup.
