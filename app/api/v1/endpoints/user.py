from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.core.security import get_current_user_id
from app.services.user_service import UserService
from app.schemas.user import UserMeResponse
from app.repositories.user_repository import UserRepository
from app.core.responses import success

router = APIRouter()


@router.get("/me", response_model=dict, summary="Get current user")
async def me(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    user = await service.get_user_by_id(user_id)
    return success(data=UserMeResponse.model_validate(user))
