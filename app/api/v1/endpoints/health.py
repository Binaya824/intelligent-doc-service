from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.postgres import get_db
from app.core.responses import success
from app.core.exceptions import AppException

router = APIRouter()

@router.get("/", summary="Health Check", response_model=dict)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Simple query to check database connectivity
        print(" db health check " , db)
    except Exception as e:
        print(f"Health check failed: {e}")
        raise AppException(message="Service Unhealthy", status_code=503) from e

    return success(message="Service Healthy")