FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    TRUST_PROXY_HEADERS=true

# Hugging Face Spaces runs containers as UID 1000.
RUN useradd --create-home --uid 1000 user
USER user
ENV PATH=/home/user/.local/bin:$PATH
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user app ./app
COPY --chown=user data ./data

# Writable data folder (SQLite, vector index). Ephemeral on the free Space tier.
RUN mkdir -p storage

# Download the embedding model at build time so the first request is fast.
# The Chroma index is built from /data at startup (the free Space disk is ephemeral).
RUN python -c "from app.config import get_settings; from app.rag.embeddings import FastEmbedder; s = get_settings(); FastEmbedder(s.embedding_model, s.embedding_cache_dir)"

EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
