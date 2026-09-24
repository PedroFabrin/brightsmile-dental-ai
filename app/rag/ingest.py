"""Rebuild the vector index from the Markdown files in `data/`.

Usage: python -m app.rag.ingest
"""

import logging
from pathlib import Path

from app.config import get_settings
from app.rag.service import get_embedder, get_store, ingest

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    total = ingest(Path(get_settings().data_dir), get_embedder(), get_store())
    print(f"Indexed {total} chunks")
