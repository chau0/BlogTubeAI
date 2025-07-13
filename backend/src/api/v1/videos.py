from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.schemas import VideoRequest, VideoResponse, JobResponse
from ...services.video_service import VideoService
from ...services.job_service import JobService

router = APIRouter()


@router.post("/process", response_model=JobResponse)
async def process_video(
    video_request: VideoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start processing a YouTube video"""
    video_service = VideoService(db)
    job_service = JobService(db)
    
    # Validate YouTube URL
    if not video_service.validate_youtube_url(video_request.url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Create processing job
    job = job_service.create_job(video_request)
    
    # Start background processing
    background_tasks.add_task(
        video_service.process_video_async,
        job.id,
        video_request
    )
    
    return JobResponse.from_orm(job)


@router.get("/info")
async def get_video_info(url: str):
    """Get YouTube video information"""
    video_service = VideoService()
    
    if not video_service.validate_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        info = video_service.get_video_info(url)
        return VideoResponse(**info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
