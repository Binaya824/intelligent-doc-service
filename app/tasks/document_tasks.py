import asyncio
from uuid import UUID
from app.core.celery_app import celery_app
from app.db.postgres import AsyncSessionLocal
from app.repositories.document_repository import DocumentRepository
from app.services.assistant_service import AssistantService


@celery_app.task(
    bind=True,
    name="app.tasks.document_tasks.process_document",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def process_document(self, document_id: UUID):
    """
    Celery task runs in a worker process.
    Must explicitly manage async DB calls.
    """

    async def _run():
        async with AsyncSessionLocal() as db:
            repo = DocumentRepository(db)

            # processing
            await repo.update_status(document_id, "processing")
            doc = await repo.get_by_id(document_id)
            print(f"Document retrieved: {doc.pages_json}")

            # TODO:
            assistant = AssistantService()
            assistant.create_embeddings(
                collection_name=str(document_id),
                pages=doc.pages_json,
            )
            # - push to Qdrant
            print(f"Processing document ID: {document_id}")

            await repo.update_status(document_id, "ready")

    asyncio.run(_run())
