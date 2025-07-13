from enum import Enum


class JobStatus(str, Enum):
    """Job processing status"""
    PENDING = "pending"
    VALIDATING = "validating"
    FETCHING_TRANSCRIPT = "fetching_transcript"
    GENERATING_BLOG = "generating_blog"
    FORMATTING = "formatting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobStep(str, Enum):
    """Job processing steps"""
    VALIDATE_URL = "validate_url"
    FETCH_VIDEO_INFO = "fetch_video_info"
    DETECT_LANGUAGES = "detect_languages"
    FETCH_TRANSCRIPT = "fetch_transcript"
    GENERATE_CONTENT = "generate_content"
    FORMAT_BLOG = "format_blog"
    SAVE_OUTPUT = "save_output"


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"


class BlogStyle(str, Enum):
    """Blog post styles"""
    TECHNICAL = "technical"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    ACADEMIC = "academic"
    CREATIVE = "creative"


class ErrorCode(str, Enum):
    """Error codes for structured error handling"""
    VIDEO_NOT_FOUND = "VIDEO_NOT_FOUND"
    TRANSCRIPT_UNAVAILABLE = "TRANSCRIPT_UNAVAILABLE"
    LANGUAGE_NOT_SUPPORTED = "LANGUAGE_NOT_SUPPORTED"
    LLM_API_ERROR = "LLM_API_ERROR"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    NETWORK_ERROR = "NETWORK_ERROR"
    INVALID_URL = "INVALID_URL"
    PROCESSING_TIMEOUT = "PROCESSING_TIMEOUT"
    INSUFFICIENT_CREDITS = "INSUFFICIENT_CREDITS"
