"""Job repository for database operations"""

from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from ..models import Job
from ...models.schemas import JobResponse, JobStatus


class JobRepository(BaseRepository[Job]):
    """Repository for job-related database operations"""
    
    def __init__(self):
        super().__init__(Job)
    
    async def get_by_status(self, status: JobStatus, limit: int = 100) -> List[Job]:
        """Get jobs by status"""
        async with get_db_session() as session:
            result = await session.execute(
                select(Job).where(Job.status == status.value).limit(limit)
            )
            return result.scalars().all()
    
    async def get_active_jobs(self) -> List[Job]:
        """Get all active (non-terminal) jobs"""
        active_statuses = [
            JobStatus.PENDING.value,
            JobStatus.VALIDATING.value,
            JobStatus.FETCHING_TRANSCRIPT.value,
            JobStatus.GENERATING_BLOG.value,
            JobStatus.FORMATTING.value
        ]
        
        async with get_db_session() as session:
            result = await session.execute(
                select(Job).where(Job.status.in_(active_statuses))
            )
            return result.scalars().all()
    
    async def get_jobs_by_provider(self, provider: str, limit: int = 100) -> List[Job]:
        """Get jobs by LLM provider"""
        async with get_db_session() as session:
            result = await session.execute(
                select(Job).where(Job.llm_provider == provider).limit(limit)
            )
            return result.scalars().all()
    
    async def count_jobs_by_status(self) -> dict:
        """Count jobs grouped by status"""
        # This would implement status counting
        pass