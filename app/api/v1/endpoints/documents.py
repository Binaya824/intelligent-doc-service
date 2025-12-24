from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.core.security import get_current_user_id
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.schemas.document import DocumentUploadResponse , DocumentQueryRequest, DocumentQueryResponse
from app.core.responses import success
from uuid import UUID
from app.services.assistant_service import AssistantService

router = APIRouter()

@router.post("/upload", summary="Upload document")
async def upload_document(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()

    service = DocumentService(DocumentRepository(db))
    doc = await service.upload(
        user_id=user_id,
        filename=file.filename,
        file_bytes=content,
    )

    return success(
        data=DocumentUploadResponse(
            id=doc.id,
            filename=doc.filename,
            status=doc.status,
            pages=doc.pages_json,
        )
    )
    
    

@router.post(
    "/{id}/query",
    summary="Query a document",
)
async def query_document(
    id: UUID,
    payload: DocumentQueryRequest,
    user_id=Depends(get_current_user_id),
):
    """
    Query a document by ID using natural language.
    """

    assistant = AssistantService()
    answer = assistant.rag_query(
        collection_name=str(id),
        query=payload.query,
    )

    return success(
        data=DocumentQueryResponse(
            document_id=id,
            answer=answer,
        )
    )
