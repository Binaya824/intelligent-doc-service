from typing import List
from app.schemas.document import PageData
from app.schemas.chunk import Chunk


def chunk_page(
    page: PageData,
    chunk_size: int = 1000,
    overlap: int = 200,
) -> List[Chunk]:
    """
    Chunk a single page with overlap.
    - Does NOT cross page boundaries
    - Deterministic
    """

    assert chunk_size > overlap, "chunk_size must be > overlap"

    # 1. Merge all text blocks into one string
    full_text = "\n".join(t.strip() for t in page["texts"] if t.strip())

    if not full_text:
        return []

    chunks: List[Chunk] = []

    start = 0
    chunk_index = 0
    text_length = len(full_text)

    while start < text_length:
        end = start + chunk_size
        chunk_text = full_text[start:end]

        chunks.append(
            Chunk(
                page=page["page"],
                chunk_index=chunk_index,
                text=chunk_text,
            )
        )

        chunk_index += 1
        start = end - overlap

        if start < 0:
            start = 0

    return chunks
