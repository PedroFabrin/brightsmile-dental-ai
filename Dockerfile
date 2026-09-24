FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

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

# Phase 2 adds here: download the fastembed model and build the Chroma index from /data.

EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
