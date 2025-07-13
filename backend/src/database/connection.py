"""Database connection and session management"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from ..web.config import get_settings

Base = declarative_base()
engine = None
async_session_maker = None


async def init_db():
    """Initialize database connection"""
    global engine, async_session_maker
    
    settings = get_settings()
    
    # Convert SQLite URL for async usage
    database_url = settings.database_url
    if database_url.startswith("sqlite:///"):
        database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    
    engine = create_async_engine(
        database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
    )
    
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency"""
    if async_session_maker is None:
        await init_db()
    
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


# For compatibility with existing code
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database dependency for FastAPI"""
    async for session in get_db_session():
        yield session