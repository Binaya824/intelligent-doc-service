# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import documents, health ,auth , user

router = APIRouter(prefix="/v1")

router.include_router(documents.router, prefix="/documents", tags=["Documents"])
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    user.router,
    prefix="/users",
    tags=["Users"],
)
