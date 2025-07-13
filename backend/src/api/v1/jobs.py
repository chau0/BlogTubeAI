from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.schemas import JobResponse, JobStatus
from ...services.job_service import JobService

router = APIRouter()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """Get job status and details"""
    job_service = JobService(db)
    job = job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse.from_orm(job)


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    status: JobStatus = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List jobs with optional filtering"""
    job_service = JobService(db)
    jobs = job_service.list_jobs(status=status, limit=limit, offset=offset)
    
    return [JobResponse.from_orm(job) for job in jobs]


@router.delete("/{job_id}")
async def cancel_job(job_id: str, db: Session = Depends(get_db)):
    """Cancel a running job"""
    job_service = JobService(db)
    
    if not job_service.cancel_job(job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"message": "Job cancelled successfully"}
