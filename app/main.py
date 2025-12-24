# app/main.py
from fastapi import FastAPI
from app.api.router import router
from app.core.error_handlers import app_exception_handler
from app.core.exceptions import AppException

def create_app() -> FastAPI:
    app = FastAPI(title="Intelligent Doc Service")

    app.include_router(router)
    app.add_exception_handler(AppException, app_exception_handler)

    return app

app = create_app()
