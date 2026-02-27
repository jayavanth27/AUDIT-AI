"""Database initialization and session helpers."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


# asynchronous engine for postgres
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# factory for async sessions
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


def get_db():
    """Dependency that yields an async session and closes it afterwards."""
    async with async_session() as session:
        yield session
