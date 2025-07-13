"""Job management service"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..core.job_manager import JobManager
from ..models.schemas import JobCreateRequest, JobResponse, JobProgress
from ..models.enums import JobStatus
from ..database.repositories.job_repository import JobRepository
from .video_service import VideoService
from .provider_service import ProviderService


class JobService:
    """Service for job-related operations"""
    
    def __init__(self):
        self.job_manager = JobManager()
        self.job_repository = JobRepository()
        self.video_service = VideoService()
        self.provider_service = ProviderService()
    
    async def create_job(self, request: JobCreateRequest) -> JobResponse:
        """Create a new video processing job"""
        # Validate video URL
        if not self.video_service.validate_youtube_url(request.video_url):
            raise ValueError("Invalid YouTube URL")
        
        # Validate provider
        if not self.provider_service.is_provider_supported(request.llm_provider):
            raise ValueError(f"Unsupported provider: {request.llm_provider}")
        
        # Create job through job manager
        job_id = await self.job_manager.create_job(request)
        
        # Get the created job
        job = await self.job_manager.get_job(job_id)
        if not job:
            raise RuntimeError("Failed to create job")
        
        # Start job processing if system can accept it
        if self.job_manager.can_accept_new_job():
            await self.job_manager.start_job(job_id)
        
        return job
    
    async def get_job(self, job_id: str) -> Optional[JobResponse]:
        """Get job by ID"""
        return await self.job_manager.get_job(job_id)
    
    async def get_jobs(self, status: Optional[JobStatus] = None, 
                      provider: Optional[str] = None,
                      limit: int = 100, offset: int = 0) -> List[JobResponse]:
        """Get jobs with optional filtering"""
        if status:
            return await self.job_repository.get_by_status(status, limit)
        elif provider:
            return await self.job_repository.get_jobs_by_provider(provider, limit)
        else:
            return await self.job_repository.get_all(limit, offset)
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job"""
        return await self.job_manager.cancel_job(job_id)
    
    async def retry_job(self, job_id: str) -> Optional[JobResponse]:
        """Retry a failed job"""
        original_job = await self.job_manager.get_job(job_id)
        if not original_job or original_job.status != JobStatus.FAILED:
            return None
        
        # Create new job with same parameters
        retry_request = JobCreateRequest(
            video_url=original_job.video_url,
            language_code=original_job.language_code,
            llm_provider=original_job.llm_provider,
            llm_model=original_job.llm_model,
            priority=1  # Give retry jobs higher priority
        )
        
        return await self.create_job(retry_request)
    
    async def get_job_progress(self, job_id: str) -> List[JobProgress]:
        """Get detailed progress for a job"""
        # This would fetch from job_progress table
        # For now, return mock data
        return []
    
    async def get_job_result(self, job_id: str) -> Optional[str]:
        """Get the result content for a completed job"""
        job = await self.get_job(job_id)
        if not job or job.status != JobStatus.COMPLETED:
            return None
        
        if not job.output_file_path:
            return None
        
        # Read the output file
        from ..core.file_manager import FileManager
        file_manager = FileManager()
        return await file_manager.read_file(job.output_file_path)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "active_jobs": self.job_manager.get_active_job_count(),
            "can_accept_jobs": self.job_manager.can_accept_new_job(),
            "max_concurrent_jobs": self.job_manager.max_concurrent_jobs
        }