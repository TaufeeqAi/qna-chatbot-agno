# backend/app/utils/pdf_utils.py

import io
from typing import List
from PyPDF2 import PdfReader
from .vector_client import VectorClient

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Read PDF bytes and return the full concatenated text.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    text_pages: List[str] = []
    for page in reader.pages:
        text_pages.append(page.extract_text() or "")
    return "\n".join(text_pages)

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[str]:
    """
    Split `text` into chunks of `chunk_size` characters with `overlap`.
    """
    chunks: List[str] = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        # Move start forward but leave overlap
        start += chunk_size - overlap
    return chunks

def ingest_pdf(
    file_bytes: bytes,
    user_id: int,
    vector_db_url: str,
    vector_api_key: str
) -> None:
    """
    Full pipeline:
      1. Extract text from PDF bytes
      2. Chunk text
      3. Upsert chunks into user-scoped vector index
    """
    # 1. Extract
    full_text = extract_text_from_pdf(file_bytes)

    # 2. Chunk
    chunks = chunk_text(full_text, chunk_size=1000, overlap=200)

    # 3. Upsert
    vc = VectorClient(
        user_id=user_id,
        api_key=vector_api_key,
        environment=vector_db_url
    )
    vc.upsert_chunks(chunks)
