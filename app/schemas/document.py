from pydantic import BaseModel
from pydantic import ConfigDict
from typing import List
from uuid import UUID

class PageData(BaseModel):
    page: int
    texts: List[str]

    model_config = ConfigDict(from_attributes=True)


class DocumentUploadResponse(BaseModel):
    id: UUID
    filename: str
    status: str
    pages: List[PageData]

    model_config = ConfigDict(from_attributes=True)


class DocumentQueryRequest(BaseModel):
    query: str


class DocumentQueryResponse(BaseModel):
    document_id: UUID
    answer: str