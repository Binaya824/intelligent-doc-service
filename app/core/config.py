from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "intelligent-doc-service"
    ENV: str = "local"

    DATABASE_URL: str
    QDRANT_URL: str
    QDRANT_API_KEY: str | None = None

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EMBEDDINGS_MODEL: str
    API_KEY: str
    BASE_URL: str

    CHAT_MODEL: str



    class Config:
        env_file = ".env"


settings = Settings()
