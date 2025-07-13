"""Base repository with common database operations"""

from typing import TypeVar, Generic, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import declarative_base

from ..connection import get_db_session

Base = declarative_base()
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, model: ModelType):
        self.model = model
    
    async def create(self, obj: ModelType) -> ModelType:
        """Create a new record"""
        async with get_db_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    
    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get record by ID"""
        async with get_db_session() as session:
            result = await session.execute(select(self.model).where(self.model.id == id))
            return result.scalar_one_or_none()
    
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Get all records with pagination"""
        async with get_db_session() as session:
            result = await session.execute(
                select(self.model).limit(limit).offset(offset)
            )
            return result.scalars().all()
    
    async def update(self, obj: ModelType) -> ModelType:
        """Update an existing record"""
        async with get_db_session() as session:
            await session.merge(obj)
            await session.commit()
            return obj
    
    async def delete_by_id(self, id: str) -> bool:
        """Delete record by ID"""
        async with get_db_session() as session:
            result = await session.execute(
                delete(self.model).where(self.model.id == id)
            )
            await session.commit()
            return result.rowcount > 0