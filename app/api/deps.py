from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.repositories.user_repository import UserRepository
from app.core.security import decode_access_token
from app.core.exceptions import AppException

async def get_current_user_id(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> int:
    if not authorization.startswith("Bearer "):
        raise AppException("Invalid authorization header", 401)

    token = authorization.split(" ")[1]

    try:
        user_id = decode_access_token(token)
    except Exception:
        raise AppException("Invalid or expired token", 401)

    # Optional: verify user still exists
    repo = UserRepository(db)
    if not await repo.get_by_email:  # just existence check
        pass

    return user_id
