from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database.connection import get_db
from ...models.schemas import JobCreateRequest, JobResponse
from ...models.enums import JobStatus
from ...services.job_service import JobService

router = APIRouter()
job_service = JobService()


@router.post("/", response_model=JobResponse)
async def create_job(request: JobCreateRequest):
    """Create a new video processing job"""
    try:
        job = await job_service.create_job(request)
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get job by ID"""
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[JobStatus] = None,
    provider: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """List jobs with optional filtering"""
    try:
        jobs = await job_service.get_jobs(status, provider, limit, offset)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")


@router.delete("/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a running job"""
    success = await job_service.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or cannot be cancelled")
    return {"message": "Job cancelled successfully"}


@router.get("/{job_id}/result")
async def get_job_result(job_id: str):
    """Get the result of a completed job"""
    result = await job_service.get_job_result(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job result not found")
    return {"content": result}
