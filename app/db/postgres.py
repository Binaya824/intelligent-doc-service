from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.engine.url import make_url
from app.core.config import settings

try:
    print("Creating database engine with URL:", settings.DATABASE_URL)
    print("Parsed URL:", make_url(settings.DATABASE_URL))
    engine = create_async_engine(
        make_url(settings.DATABASE_URL),
        pool_pre_ping=True,
    )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
