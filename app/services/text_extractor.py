import fitz  # PyMuPDF
from typing import List, Dict

def extract_text_pagewise(file_bytes: bytes) -> List[Dict]:
    """
    Extract text from PDF page-wise.
    Each page contains multiple text blocks.
    """

    doc = fitz.open(stream=file_bytes, filetype="pdf")

    pages_data = []

    for page_index, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")

        texts: List[str] = []

        for block in blocks:
            text = block[4].strip()  # block[4] is text
            if text:
                texts.append(text)

        pages_data.append({
            "page": page_index,
            "texts": texts
        })

    doc.close()
    return pages_data
