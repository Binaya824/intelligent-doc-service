from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.responses import success

router = APIRouter()

@router.post("/register")
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))
    user = await service.register(payload.email, payload.password)
    return success({"id": user.id, "email": user.email})

@router.post("/login")
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))
    token = await service.login(payload.email, payload.password)
    return success({"access_token": token})
