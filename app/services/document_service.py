from app.repositories.document_repository import DocumentRepository
from app.services.text_extractor import extract_text_pagewise
from app.tasks.document_tasks import process_document
import json

class DocumentService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    async def upload(
        self,
        user_id: int,
        filename: str,
        file_bytes: bytes,
    ):
        pages = extract_text_pagewise(file_bytes)
        
        print("++++++++++" , json.dumps(pages, indent=4))

        doc =  await self.repo.create(
            user_id=user_id,
            filename=filename,
            pages_json=pages,
        )
        task = process_document.apply_async(
            args=[doc.id],
            queue="pdf_processing",
            routing_key="pdf_processing",
        )
        print("Celery Task ID:", task.id)
        
        return doc
