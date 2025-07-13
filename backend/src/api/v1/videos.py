from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.schemas import VideoRequest, VideoResponse, JobResponse, VideoValidationResponse
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


@router.get("/{video_id}/info", response_model=VideoResponse)
async def get_video_info_by_id(video_id: str):
    """Get detailed YouTube video information by video ID"""
    video_service = VideoService()
    
    # Validate video ID format
    if not video_id or len(video_id) != 11:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    
    try:
        info = await video_service.get_video_info(video_id)
        
        return VideoResponse(
            title=info["title"],
            duration=0,  # oEmbed doesn't provide duration
            thumbnail=info["thumbnail_url"],
            description=None  # oEmbed doesn't provide description
        )
    except ValueError as e:
        # Client errors (video not found, private, region restricted)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Server errors (quota, network issues)
        error_msg = str(e)
        if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            raise HTTPException(status_code=429, detail=str(e))
        else:
            raise HTTPException(status_code=503, detail=str(e))


@router.get("/{video_id}/validate", response_model=VideoValidationResponse)
async def validate_video(video_id: str):
    """Validate video availability and get basic info"""
    video_service = VideoService()
    
    # Validate video ID format
    if not video_id or len(video_id) != 11:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    
    try:
        validation_result = await video_service.validate_video_availability(video_id)
        
        video_info = None
        available_languages = []
        
        if validation_result["is_available"]:
            # Convert to VideoInfo schema format
            info = validation_result["video_info"]
            from ...models.schemas import VideoInfo
            video_info = VideoInfo(
                video_id=video_id,
                title=info["title"],
                duration=None,
                thumbnail=info["thumbnail_url"],
                channel=info["author_name"],
                upload_date=None,
                view_count=None,
                description=None
            )
            
            # TODO: Fetch available languages using transcript_handler
            # This would be implemented when language detection is added
        
        return VideoValidationResponse(
            is_valid=validation_result["is_available"],
            video_info=video_info,
            available_languages=available_languages,
            error_message=validation_result["error"]
        )
        
    except Exception as e:
        return VideoValidationResponse(
            is_valid=False,
            video_info=None,
            available_languages=[],
            error_message=f"Validation failed: {str(e)}"
        )
