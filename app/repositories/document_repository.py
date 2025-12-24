from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update , select
from app.models.document import Document

class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: int,
        filename: str,
        pages_json: list,
    ) -> Document:
        doc = Document(
            user_id=user_id,
            filename=filename,
            status="uploaded",
            pages_json=pages_json,
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc

    async def get_by_id(self, document_id: int) -> Document | None:   
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalars().first() 
    
    async def update_status(self, document_id: int, status: str):
        await self.db.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(status=status)
        )
        await self.db.commit()