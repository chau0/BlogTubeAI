from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from .enums import JobStatus, JobStep, LLMProvider, ErrorCode


class VideoRequest(BaseModel):
    """Request schema for video processing"""
    url: HttpUrl
    provider: LLMProvider
    model: str
    style: str = "technical"
    custom_prompt: Optional[str] = None
    
    @validator('url')
    def validate_youtube_url(cls, v):
        url_str = str(v)
        if 'youtube.com' not in url_str and 'youtu.be' not in url_str:
            raise ValueError('Must be a YouTube URL')
        return v


class VideoResponse(BaseModel):
    """Response schema for video information"""
    title: str
    duration: int
    thumbnail: str
    description: Optional[str] = None


class JobCreateRequest(BaseModel):
    """Request schema for creating a new job"""
    video_url: str = Field(..., description="YouTube video URL")
    language_code: str = Field(..., description="Transcript language code")
    llm_provider: str = Field(..., description="LLM provider identifier")
    llm_model: Optional[str] = Field(None, description="Specific model name")
    custom_prompt: Optional[str] = Field(None, description="Custom generation prompt")
    output_format: str = Field("markdown", description="Output format")
    priority: int = Field(0, description="Job priority (0=normal, 1=high)")
    
    @validator('video_url')
    def validate_youtube_url(cls, v):
        if 'youtube.com' not in v and 'youtu.be' not in v:
            raise ValueError('Must be a YouTube URL')
        return v


class JobResponse(BaseModel):
    """Response schema for job information"""
    id: str
    video_id: str
    video_url: str
    video_title: Optional[str]
    video_duration: Optional[int]
    video_thumbnail: Optional[str]
    language_code: str
    language_name: Optional[str]
    llm_provider: str
    llm_model: Optional[str]
    status: JobStatus
    priority: int
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    error_code: Optional[str]
    retry_count: int
    processing_time_seconds: Optional[int]
    output_file_path: Optional[str]
    
    class Config:
        from_attributes = True


class JobProgress(BaseModel):
    """Schema for job progress tracking"""
    job_id: str
    step: JobStep
    status: str
    message: Optional[str]
    progress_percentage: int
    details: Optional[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime]
    error_details: Optional[str]


class VideoInfo(BaseModel):
    """Video information schema"""
    video_id: str
    title: str
    duration: Optional[int]
    thumbnail: Optional[str]
    channel: Optional[str]
    upload_date: Optional[str]
    view_count: Optional[int]
    description: Optional[str]


class LanguageInfo(BaseModel):
    """Language information schema"""
    code: str
    name: str
    is_auto_generated: bool
    is_translatable: bool
    confidence: Optional[float]


class ProviderInfo(BaseModel):
    """LLM provider information schema"""
    name: str
    display_name: str
    description: str
    models: List[str]
    is_available: bool
    features: List[str]
    pricing_tier: str
    rate_limits: Dict[str, int]
    last_health_check: Optional[datetime]


class WebSocketMessage(BaseModel):
    """WebSocket message schema"""
    type: str
    job_id: str
    data: Dict[str, Any]
    timestamp: datetime


class ProgressUpdate(BaseModel):
    """Progress update schema"""
    job_id: str
    step: JobStep
    status: str
    progress: int
    message: str
    estimated_remaining: Optional[int]


class APIError(BaseModel):
    """API error response schema"""
    error: str
    message: str
    details: Optional[Dict]
    request_id: str
    timestamp: datetime
    suggestions: List[str]


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    message: str
    database: str
    version: str
    uptime_seconds: int


class SystemStats(BaseModel):
    """System statistics schema"""
    active_jobs: int
    total_jobs_today: int
    average_processing_time: float
    provider_health: Dict[str, bool]
    cache_stats: Dict[str, Any]


class VideoValidationResponse(BaseModel):
    """Video URL validation response"""
    is_valid: bool
    video_info: Optional[VideoInfo]
    available_languages: List[LanguageInfo]
    error_message: Optional[str]
