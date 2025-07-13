"""Job lifecycle management"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Optional, Set
from enum import Enum

from ..models.schemas import JobStatus, JobResponse, JobCreateRequest
from ..models.enums import JobStep
from ..database.repositories.job_repository import JobRepository
from ..services.notification_service import NotificationService


class JobManager:
    """Manages job lifecycle and status tracking"""
    
    def __init__(self):
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.job_registry: Dict[str, JobResponse] = {}
        self.job_repository = JobRepository()
        self.notification_service = NotificationService()
        self.max_concurrent_jobs = 5
        
    async def create_job(self, request: JobCreateRequest) -> str:
        """Create a new job and return job ID"""
        job_id = str(uuid.uuid4())
        
        # Create job record
        job = JobResponse(
            id=job_id,
            video_id="",  # Will be extracted during processing
            video_url=request.video_url,
            video_title=None,
            video_duration=None,
            video_thumbnail=None,
            language_code=request.language_code,
            language_name=None,
            llm_provider=request.llm_provider,
            llm_model=request.llm_model,
            status=JobStatus.PENDING,
            priority=request.priority,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            started_at=None,
            completed_at=None,
            error_message=None,
            error_code=None,
            retry_count=0,
            processing_time_seconds=None,
            output_file_path=None
        )
        
        # Save to database
        await self.job_repository.create(job)
        self.job_registry[job_id] = job
        
        return job_id
    
    async def start_job(self, job_id: str) -> bool:
        """Start processing a job"""
        if len(self.active_jobs) >= self.max_concurrent_jobs:
            return False
            
        if job_id not in self.job_registry:
            return False
            
        # Import here to avoid circular dependency
        from .background_tasks import BackgroundTaskProcessor
        
        processor = BackgroundTaskProcessor(self)
        task = asyncio.create_task(processor.process_job(job_id))
        self.active_jobs[job_id] = task
        
        # Update job status
        await self.update_job_status(job_id, JobStatus.VALIDATING)
        
        return True
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job"""
        if job_id in self.active_jobs:
            task = self.active_jobs[job_id]
            task.cancel()
            del self.active_jobs[job_id]
            
            await self.update_job_status(job_id, JobStatus.CANCELLED)
            return True
        
        return False
    
    async def get_job(self, job_id: str) -> Optional[JobResponse]:
        """Get job by ID"""
        if job_id in self.job_registry:
            return self.job_registry[job_id]
        
        # Try to load from database
        job = await self.job_repository.get_by_id(job_id)
        if job:
            self.job_registry[job_id] = job
        
        return job
    
    async def update_job_status(self, job_id: str, status: JobStatus, 
                              error_message: Optional[str] = None) -> None:
        """Update job status and notify clients"""
        if job_id not in self.job_registry:
            return
            
        job = self.job_registry[job_id]
        job.status = status
        job.updated_at = datetime.now()
        
        if error_message:
            job.error_message = error_message
            
        if status == JobStatus.COMPLETED:
            job.completed_at = datetime.now()
            if job.started_at:
                job.processing_time_seconds = int(
                    (job.completed_at - job.started_at).total_seconds()
                )
            
            # Remove from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
        
        # Save to database
        await self.job_repository.update(job)
        
        # Notify clients via WebSocket
        await self.notification_service.broadcast_job_update(job_id, {
            "status": status.value,
            "message": error_message,
            "updated_at": job.updated_at.isoformat()
        })
    
    async def cleanup_completed_jobs(self) -> None:
        """Clean up old completed jobs"""
        # This would implement cleanup logic
        pass
    
    def get_active_job_count(self) -> int:
        """Get number of currently active jobs"""
        return len(self.active_jobs)
    
    def can_accept_new_job(self) -> bool:
        """Check if system can accept new jobs"""
        return len(self.active_jobs) < self.max_concurrent_jobs