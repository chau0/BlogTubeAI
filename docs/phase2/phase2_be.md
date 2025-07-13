# Phase 2: Backend Design for BlogTubeAI Web Interface

## Overview
This document outlines the detailed backend architecture for the FastAPI web interface that will complement the existing CLI functionality. The backend will provide RESTful APIs and WebSocket connections to support a modern React frontend while reusing the existing core modules.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Folder Structure](#folder-structure)
3. [Key Components](#key-components)
4. [Database Design](#database-design)
5. [API Design](#api-design)
6. [WebSocket Architecture](#websocket-architecture)
7. [Job Processing Workflow](#job-processing-workflow)
8. [Error Handling Strategy](#error-handling-strategy)
9. [Security Considerations](#security-considerations)
10. [Performance Optimization](#performance-optimization)
11. [Integration Points](#integration-points)

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Web Application                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   REST API  │  │  WebSocket  │  │ Static File │  │  CORS   │ │
│  │  Endpoints  │  │   Handler   │  │   Serving   │  │Middleware│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    Job      │  │  Background │  │  Database   │  │  Cache  │ │
│  │  Manager    │  │    Tasks    │  │   Manager   │  │ Manager │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                 Existing Core Modules (Reused)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   YouTube   │  │ Transcript  │  │     LLM     │  │  Blog   │ │
│  │   Parser    │  │   Handler   │  │  Providers  │  │Formatter│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Modularity**: Clear separation between web layer and core business logic
2. **Reusability**: Maximum reuse of existing CLI modules
3. **Scalability**: Async/await pattern for non-blocking operations
4. **Reliability**: Comprehensive error handling and recovery mechanisms
5. **Observability**: Detailed logging and monitoring capabilities
6. **Security**: Input validation, rate limiting, and secure API key handling

---

## Folder Structure

```
backend/
├── src/
│   ├── web/                          # Web-specific modules
│   │   ├── __init__.py
│   │   ├── app.py                    # FastAPI application factory
│   │   ├── config.py                 # Web-specific configuration
│   │   └── middleware/               # Custom middleware
│   │       ├── __init__.py
│   │       ├── cors.py               # CORS configuration
│   │       ├── rate_limit.py         # Rate limiting
│   │       └── logging.py            # Request logging
│   │
│   ├── api/                          # API route definitions
│   │   ├── __init__.py
│   │   ├── v1/                       # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py             # Main API router
│   │   │   ├── videos.py             # Video-related endpoints
│   │   │   ├── jobs.py               # Job management endpoints
│   │   │   ├── providers.py          # LLM provider endpoints
│   │   │   └── health.py             # Health check endpoints
│   │   └── websocket/                # WebSocket handlers
│   │       ├── __init__.py
│   │       ├── manager.py            # WebSocket connection manager
│   │       └── handlers.py           # WebSocket event handlers
│   │
│   ├── core/                         # Core business logic (web layer)
│   │   ├── __init__.py
│   │   ├── job_manager.py            # Job lifecycle management
│   │   ├── background_tasks.py       # Background task processing
│   │   ├── cache_manager.py          # Caching layer
│   │   └── file_manager.py           # File operations for web
│   │
│   ├── models/                       # Data models and schemas
│   │   ├── __init__.py
│   │   ├── database.py               # SQLAlchemy models
│   │   ├── schemas.py                # Pydantic schemas
│   │   ├── enums.py                  # Enum definitions
│   │   └── validators.py             # Custom validators
│   │
│   ├── services/                     # Service layer
│   │   ├── __init__.py
│   │   ├── video_service.py          # Video processing service
│   │   ├── job_service.py            # Job management service
│   │   ├── provider_service.py       # LLM provider service
│   │   └── notification_service.py   # WebSocket notifications
│   │
│   ├── database/                     # Database operations
│   │   ├── __init__.py
│   │   ├── connection.py             # Database connection
│   │   ├── migrations/               # Database migrations
│   │   │   ├── __init__.py
│   │   │   ├── 001_initial.py        # Initial schema
│   │   │   └── versions/             # Migration versions
│   │   └── repositories/             # Data access layer
│   │       ├── __init__.py
│   │       ├── base.py               # Base repository
│   │       ├── job_repository.py     # Job data access
│   │       └── progress_repository.py # Progress tracking
│   │
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py               # Security utilities
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── constants.py              # Application constants
│   │   └── helpers.py                # Helper functions
│   │
│   └── ...existing CLI modules...    # Reused from Phase 1
│       ├── youtube_parser.py
│       ├── transcript_handler.py
│       ├── llm_providers.py
│       ├── blog_formatter.py
│       └── utils.py
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   ├── unit/                         # Unit tests
│   │   ├── test_api/                 # API endpoint tests
│   │   ├── test_services/            # Service layer tests
│   │   └── test_models/              # Model tests
│   ├── integration/                  # Integration tests
│   │   ├── test_job_workflow.py      # End-to-end job tests
│   │   ├── test_websocket.py         # WebSocket tests
│   │   └── test_database.py          # Database tests
│   └── fixtures/                     # Test fixtures
│       ├── sample_videos.json
│       └── mock_responses.json
│
├── alembic/                          # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── static/                           # Static files (for production)
│   └── frontend/                     # Built React app
│
├── requirements/                     # Dependency management
│   ├── base.txt                      # Core dependencies
│   ├── web.txt                       # Web-specific dependencies
│   ├── dev.txt                       # Development dependencies
│   └── test.txt                      # Testing dependencies
│
├── scripts/                          # Utility scripts
│   ├── start_dev.py                  # Development server
│   ├── migrate.py                    # Database migration
│   └── seed_data.py                  # Test data generation
│
├── docker/                           # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.worker             # Background task worker
│   └── docker-compose.yml
│
├── .env.example                      # Environment variables template
├── alembic.ini                       # Alembic configuration
├── pyproject.toml                    # Project configuration
└── README_backend.md                 # Backend-specific documentation
```

---

## Key Components

### 1. FastAPI Application (`src/web/app.py`)

**Responsibilities:**
- Application factory pattern for different environments
- Middleware configuration (CORS, rate limiting, logging)
- Router registration and API versioning
- Exception handlers and error responses
- Static file serving for production builds
- OpenAPI documentation configuration

**Key Features:**
- Environment-based configuration
- Graceful startup and shutdown handlers
- Health check endpoints
- API documentation at `/docs` and `/redoc`
- Metrics endpoint for monitoring

### 2. Job Manager (`src/core/job_manager.py`)

**Responsibilities:**
- Job lifecycle management (create, track, cancel, cleanup)
- UUID-based job identification
- Status tracking and progress reporting
- Resource management and cleanup
- Job queue management with priority support
- Concurrent job handling with limits

**Key Features:**
- In-memory job registry with persistence
- Job timeout and cancellation handling
- Progress tracking with step-by-step updates
- Error recovery and retry mechanisms
- Job history and analytics

### 3. Background Task Processor (`src/core/background_tasks.py`)

**Responsibilities:**
- Async task execution using FastAPI BackgroundTasks
- Integration with existing CLI modules
- Progress reporting via WebSocket
- Error handling and recovery
- Resource cleanup on completion/failure

**Processing Pipeline:**
1. **Validation Phase**: URL validation and video metadata extraction
2. **Transcript Phase**: Language detection and transcript fetching
3. **Generation Phase**: LLM content generation with progress tracking
4. **Formatting Phase**: Blog formatting and file creation
5. **Completion Phase**: Result storage and notification

### 4. WebSocket Manager (`src/api/websocket/manager.py`)

**Responsibilities:**
- WebSocket connection lifecycle management
- Client registration and deregistration
- Message broadcasting to specific clients
- Connection health monitoring
- Rate limiting and abuse prevention

**Features:**
- Connection pooling with client identification
- Heartbeat mechanism for connection health
- Automatic reconnection support
- Message queuing for offline clients
- Broadcasting patterns (unicast, multicast)

### 5. Database Manager (`src/database/connection.py`)

**Responsibilities:**
- SQLAlchemy engine and session management
- Connection pooling and lifecycle
- Migration management integration
- Transaction handling and rollback
- Query optimization and caching

**Configuration:**
- SQLite for development and testing
- PostgreSQL support for production scaling
- Connection pool sizing and timeout configuration
- Automatic reconnection handling
- Query logging and performance monitoring

### 6. Service Layer Components

#### Video Service (`src/services/video_service.py`)
- YouTube URL validation and parsing
- Video metadata extraction and caching
- Transcript language detection
- Integration with existing `youtube_parser.py` and `transcript_handler.py`

#### Job Service (`src/services/job_service.py`)
- Job creation and validation
- Status tracking and progress reporting
- Job cancellation and cleanup
- History management and analytics

#### Provider Service (`src/services/provider_service.py`)
- LLM provider management and health checking
- API key validation and testing
- Provider capability discovery
- Rate limiting and quota management

#### Notification Service (`src/services/notification_service.py`)
- WebSocket message formatting and sending
- Progress update broadcasting
- Error notification handling
- Client-specific message delivery

---

## Database Design

### Schema Overview

```sql
-- Core job tracking table
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,                    -- UUID v4
    video_id TEXT NOT NULL,                 -- YouTube video ID
    video_url TEXT NOT NULL,                -- Original YouTube URL
    video_title TEXT,                       -- Video title from YouTube
    video_duration INTEGER,                 -- Duration in seconds
    video_thumbnail TEXT,                   -- Thumbnail URL
    language_code TEXT NOT NULL,            -- Selected transcript language
    language_name TEXT,                     -- Human-readable language name
    llm_provider TEXT NOT NULL,             -- Selected LLM provider
    llm_model TEXT,                         -- Specific model used
    status TEXT NOT NULL DEFAULT 'pending', -- Job status enum
    priority INTEGER DEFAULT 0,             -- Job priority (0 = normal)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,                   -- When processing began
    completed_at TIMESTAMP,                 -- When processing completed
    error_message TEXT,                     -- Error details if failed
    error_code TEXT,                        -- Structured error code
    retry_count INTEGER DEFAULT 0,          -- Number of retry attempts
    max_retries INTEGER DEFAULT 3,          -- Maximum retry attempts
    metadata JSON,                          -- Additional job metadata
    
    -- File paths
    transcript_file_path TEXT,              -- Saved transcript location
    output_file_path TEXT,                  -- Generated blog location
    
    -- Processing metrics
    processing_time_seconds INTEGER,        -- Total processing time
    transcript_length INTEGER,              -- Transcript character count
    output_length INTEGER,                  -- Generated blog character count
    tokens_used INTEGER,                    -- LLM tokens consumed
    
    -- Indexing
    INDEX idx_jobs_status (status),
    INDEX idx_jobs_created (created_at),
    INDEX idx_jobs_video_id (video_id),
    INDEX idx_jobs_provider (llm_provider)
);

-- Job progress tracking for real-time updates
CREATE TABLE job_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    step TEXT NOT NULL,                     -- Processing step identifier
    status TEXT NOT NULL,                   -- Step status (pending, processing, completed, failed)
    message TEXT,                           -- Step-specific message
    progress_percentage INTEGER DEFAULT 0,  -- 0-100 progress indicator
    details JSON,                           -- Additional step details
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,                 -- When step completed
    error_details TEXT,                     -- Step-specific error info
    
    INDEX idx_progress_job_id (job_id),
    INDEX idx_progress_step (step),
    INDEX idx_progress_status (status)
);

-- Job step definitions and metadata
CREATE TABLE job_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_name TEXT UNIQUE NOT NULL,         -- Step identifier
    display_name TEXT NOT NULL,             -- User-friendly name
    description TEXT,                       -- Step description
    estimated_duration_seconds INTEGER,     -- Typical duration
    is_required BOOLEAN DEFAULT TRUE,       -- Whether step is mandatory
    order_index INTEGER NOT NULL,           -- Step execution order
    retry_allowed BOOLEAN DEFAULT TRUE,     -- Whether step can be retried
    
    INDEX idx_steps_order (order_index)
);

-- WebSocket connection tracking
CREATE TABLE websocket_connections (
    id TEXT PRIMARY KEY,                    -- Connection UUID
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    client_ip TEXT,                         -- Client IP address
    user_agent TEXT,                        -- Client user agent
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    INDEX idx_ws_job_id (job_id),
    INDEX idx_ws_active (is_active)
);

-- System configuration and settings
CREATE TABLE system_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    value_type TEXT DEFAULT 'string',      -- string, integer, boolean, json
    description TEXT,
    is_secret BOOLEAN DEFAULT FALSE,       -- For sensitive config
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LLM provider status and health
CREATE TABLE provider_status (
    provider_name TEXT PRIMARY KEY,
    is_available BOOLEAN DEFAULT TRUE,
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INTEGER,
    error_message TEXT,
    quota_remaining INTEGER,
    quota_reset_at TIMESTAMP,
    
    INDEX idx_provider_available (is_available)
);

-- Audit log for important operations
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT REFERENCES jobs(id),
    action TEXT NOT NULL,                   -- Action performed
    details JSON,                           -- Action details
    client_ip TEXT,                         -- Client IP
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_audit_job (job_id),
    INDEX idx_audit_timestamp (timestamp)
);
```

### Data Models (Pydantic Schemas)

#### Job-Related Models

```python
# Job status enumeration
class JobStatus(str, Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    FETCHING_TRANSCRIPT = "fetching_transcript"
    GENERATING_BLOG = "generating_blog"
    FORMATTING = "formatting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Job step enumeration
class JobStep(str, Enum):
    VALIDATE_URL = "validate_url"
    FETCH_VIDEO_INFO = "fetch_video_info"
    DETECT_LANGUAGES = "detect_languages"
    FETCH_TRANSCRIPT = "fetch_transcript"
    GENERATE_CONTENT = "generate_content"
    FORMAT_BLOG = "format_blog"
    SAVE_OUTPUT = "save_output"

# Job creation request
class JobCreateRequest(BaseModel):
    video_url: str = Field(..., description="YouTube video URL")
    language_code: str = Field(..., description="Transcript language code")
    llm_provider: str = Field(..., description="LLM provider identifier")
    llm_model: Optional[str] = Field(None, description="Specific model name")
    custom_prompt: Optional[str] = Field(None, description="Custom generation prompt")
    output_format: str = Field("markdown", description="Output format")
    priority: int = Field(0, description="Job priority (0=normal, 1=high)")

# Job response model
class JobResponse(BaseModel):
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

# Job progress model
class JobProgress(BaseModel):
    job_id: str
    step: JobStep
    status: str
    message: Optional[str]
    progress_percentage: int
    details: Optional[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime]
    error_details: Optional[str]

# WebSocket message models
class WebSocketMessage(BaseModel):
    type: str
    job_id: str
    data: Dict[str, Any]
    timestamp: datetime

class ProgressUpdate(BaseModel):
    job_id: str
    step: JobStep
    status: str
    progress: int
    message: str
    estimated_remaining: Optional[int]
```

#### Video and Provider Models

```python
# Video information model
class VideoInfo(BaseModel):
    video_id: str
    title: str
    duration: Optional[int]
    thumbnail: Optional[str]
    channel: Optional[str]
    upload_date: Optional[str]
    view_count: Optional[int]
    description: Optional[str]

# Language information
class LanguageInfo(BaseModel):
    code: str
    name: str
    is_auto_generated: bool
    is_translatable: bool
    confidence: Optional[float]

# Provider information
class ProviderInfo(BaseModel):
    name: str
    display_name: str
    description: str
    models: List[str]
    is_available: bool
    features: List[str]
    pricing_tier: str
    rate_limits: Dict[str, int]
    last_health_check: Optional[datetime]
```

---

## API Design

### RESTful API Endpoints

#### Video Operations

```python
# Video URL validation and information
POST /api/v1/videos/validate
Request: {"url": "https://youtube.com/watch?v=..."}
Response: VideoInfo + available languages

GET /api/v1/videos/{video_id}/info
Response: Detailed video information

GET /api/v1/videos/{video_id}/languages
Response: List[LanguageInfo] with available transcript languages

GET /api/v1/videos/{video_id}/transcript
Query params: language_code, format
Response: Raw transcript content
```

#### Job Management

```python
# Job lifecycle operations
POST /api/v1/jobs
Request: JobCreateRequest
Response: JobResponse with job_id

GET /api/v1/jobs/{job_id}
Response: JobResponse with current status

GET /api/v1/jobs/{job_id}/progress
Response: List[JobProgress] with detailed step information

DELETE /api/v1/jobs/{job_id}
Response: Cancellation confirmation

GET /api/v1/jobs/{job_id}/result
Response: Generated blog content or download link

GET /api/v1/jobs
Query params: status, provider, limit, offset
Response: Paginated list of jobs

POST /api/v1/jobs/{job_id}/retry
Response: New job created from failed job
```

#### Provider Management

```python
# LLM provider operations
GET /api/v1/providers
Response: List[ProviderInfo] with availability status

GET /api/v1/providers/{provider_name}
Response: Detailed provider information

POST /api/v1/providers/{provider_name}/validate
Request: {"api_key": "...", "model": "..."}
Response: Validation result and capabilities

GET /api/v1/providers/{provider_name}/health
Response: Provider health status and metrics
```

#### System Operations

```python
# Health and status endpoints
GET /api/v1/health
Response: System health status

GET /api/v1/metrics
Response: System metrics and statistics

GET /api/v1/config
Response: Public configuration values

POST /api/v1/config
Request: Configuration updates (admin only)
Response: Updated configuration
```

### Error Response Format

```python
class APIError(BaseModel):
    error: str                    # Error type identifier
    message: str                  # Human-readable error message
    details: Optional[Dict]       # Additional error context
    request_id: str              # Request tracking ID
    timestamp: datetime          # Error timestamp
    suggestions: List[str]       # Suggested actions for resolution

# Example error responses
{
    "error": "VIDEO_NOT_FOUND",
    "message": "The specified YouTube video could not be found or is not accessible",
    "details": {
        "video_id": "abc123",
        "status_code": 404,
        "provider_message": "Video unavailable"
    },
    "request_id": "req_789xyz",
    "timestamp": "2024-01-15T10:30:00Z",
    "suggestions": [
        "Verify the video URL is correct",
        "Check if the video is public",
        "Try a different video"
    ]
}
```

---

## WebSocket Architecture

### Connection Management

#### WebSocket Endpoint Design

```python
# WebSocket connection endpoint
WS /api/v1/ws/jobs/{job_id}

# Connection flow:
1. Client connects with job_id
2. Server validates job exists and is accessible
3. Connection registered in WebSocketManager
4. Real-time updates sent for job progress
5. Connection cleaned up on job completion or disconnect
```

#### Message Protocol

```python
# Client -> Server messages
{
    "type": "subscribe",
    "job_id": "job_uuid",
    "client_id": "client_uuid"
}

{
    "type": "ping",
    "timestamp": "2024-01-15T10:30:00Z"
}

{
    "type": "cancel_job",
    "job_id": "job_uuid"
}

# Server -> Client messages
{
    "type": "job_progress",
    "job_id": "job_uuid",
    "data": {
        "step": "fetch_transcript",
        "status": "processing",
        "progress": 45,
        "message": "Downloading transcript for English...",
        "estimated_remaining": 30
    }
}

{
    "type": "job_completed",
    "job_id": "job_uuid",
    "data": {
        "status": "completed",
        "result_url": "/api/v1/jobs/job_uuid/result",
        "processing_time": 42,
        "word_count": 1247
    }
}

{
    "type": "job_failed",
    "job_id": "job_uuid",
    "data": {
        "error": "TRANSCRIPT_UNAVAILABLE",
        "message": "No transcript available for this video",
        "retry_allowed": true,
        "suggestions": ["Try a different language", "Check video settings"]
    }
}

{
    "type": "pong",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### WebSocket Manager Implementation Design

```python
class WebSocketManager:
    """
    Manages WebSocket connections and message broadcasting
    """
    
    # Connection tracking
    active_connections: Dict[str, WebSocket]  # connection_id -> websocket
    job_subscriptions: Dict[str, Set[str]]    # job_id -> set of connection_ids
    connection_metadata: Dict[str, Dict]       # connection_id -> metadata
    
    # Health monitoring
    last_ping: Dict[str, datetime]            # connection_id -> last ping time
    heartbeat_interval: int = 30              # seconds
    
    # Message queuing
    message_queue: Dict[str, List[Dict]]      # connection_id -> queued messages
    max_queue_size: int = 100
    
    async def connect(websocket: WebSocket, job_id: str) -> str
    async def disconnect(connection_id: str)
    async def send_to_connection(connection_id: str, message: Dict)
    async def broadcast_to_job(job_id: str, message: Dict)
    async def cleanup_stale_connections()
    async def handle_heartbeat(connection_id: str)
```

---

## Job Processing Workflow

### Job Lifecycle States

```python
class JobLifecycle:
    """
    Defines the complete job processing workflow
    """
    
    STATES = {
        "pending": "Job created, waiting to start",
        "validating": "Validating YouTube URL and video access",
        "fetching_info": "Retrieving video metadata",
        "detecting_languages": "Discovering available transcript languages",
        "fetching_transcript": "Downloading video transcript",
        "generating_content": "AI content generation in progress",
        "formatting": "Formatting blog post output",
        "saving": "Saving generated content to file",
        "completed": "Job successfully completed",
        "failed": "Job failed with error",
        "cancelled": "Job cancelled by user"
    }
    
    TRANSITIONS = {
        "pending": ["validating", "cancelled"],
        "validating": ["fetching_info", "failed"],
        "fetching_info": ["detecting_languages", "failed"],
        "detecting_languages": ["fetching_transcript", "failed"],
        "fetching_transcript": ["generating_content", "failed"],
        "generating_content": ["formatting", "failed"],
        "formatting": ["saving", "failed"],
        "saving": ["completed", "failed"],
        "failed": ["pending"],  # For retry
        "cancelled": [],  # Terminal state
        "completed": []   # Terminal state
    }
```

### Processing Pipeline Design

```python
class JobProcessor:
    """
    Orchestrates the job processing pipeline
    """
    
    async def process_job(job_id: str):
        """
        Main job processing workflow
        """
        
        try:
            # Initialize job tracking
            await update_job_status(job_id, "validating")
            await broadcast_progress(job_id, "validate_url", "processing", 0)
            
            # Step 1: Validate URL and extract video ID
            video_info = await validate_youtube_url(job.video_url)
            await broadcast_progress(job_id, "validate_url", "completed", 10)
            
            # Step 2: Fetch video metadata
            await update_job_status(job_id, "fetching_info")
            await broadcast_progress(job_id, "fetch_info", "processing", 15)
            
            metadata = await fetch_video_metadata(video_info.video_id)
            await update_job_progress(job_id, metadata)
            await broadcast_progress(job_id, "fetch_info", "completed", 25)
            
            # Step 3: Detect available languages
            await update_job_status(job_id, "detecting_languages")
            await broadcast_progress(job_id, "detect_languages", "processing", 30)
            
            languages = await detect_transcript_languages(video_info.video_id)
            await validate_language_selection(job.language_code, languages)
            await broadcast_progress(job_id, "detect_languages", "completed", 35)
            
            # Step 4: Fetch transcript
            await update_job_status(job_id, "fetching_transcript")
            await broadcast_progress(job_id, "fetch_transcript", "processing", 40)
            
            transcript = await fetch_transcript(
                video_info.video_id, 
                job.language_code
            )
            transcript_path = await save_transcript(job_id, transcript)
            await broadcast_progress(job_id, "fetch_transcript", "completed", 60)
            
            # Step 5: Generate blog content
            await update_job_status(job_id, "generating_content")
            await broadcast_progress(job_id, "generate_content", "processing", 65)
            
            blog_content = await generate_blog_content(
                transcript=transcript,
                provider=job.llm_provider,
                model=job.llm_model,
                custom_prompt=job.custom_prompt,
                progress_callback=lambda p: broadcast_progress(
                    job_id, "generate_content", "processing", 65 + (p * 0.25)
                )
            )
            await broadcast_progress(job_id, "generate_content", "completed", 90)
            
            # Step 6: Format and save output
            await update_job_status(job_id, "formatting")
            await broadcast_progress(job_id, "format_output", "processing", 92)
            
            formatted_blog = await format_blog_post(
                content=blog_content,
                video_info=metadata,
                format=job.output_format
            )
            
            output_path = await save_blog_output(job_id, formatted_blog)
            await broadcast_progress(job_id, "format_output", "completed", 95)
            
            # Step 7: Complete job
            await update_job_status(job_id, "completed")
            await update_job_completion(job_id, output_path, transcript_path)
            await broadcast_completion(job_id, output_path)
            
            # Cleanup temporary files if configured
            await cleanup_job_files(job_id)
            
        except CancellationError:
            await handle_job_cancellation(job_id)
        except Exception as error:
            await handle_job_failure(job_id, error)
        finally:
            await cleanup_job_resources(job_id)
```

### Error Handling and Recovery

```python
class ErrorHandler:
    """
    Comprehensive error handling for job processing
    """
    
    RETRY_STRATEGIES = {
        "NETWORK_ERROR": {
            "max_retries": 3,
            "backoff": "exponential",
            "base_delay": 5
        },
        "API_RATE_LIMIT": {
            "max_retries": 5,
            "backoff": "linear",
            "base_delay": 60
        },
        "PROVIDER_UNAVAILABLE": {
            "max_retries": 2,
            "backoff": "exponential",
            "base_delay": 30,
            "fallback_providers": True
        },
        "TRANSCRIPT_UNAVAILABLE": {
            "max_retries": 1,
            "alternative_languages": True
        }
    }
    
    async def handle_error(job_id: str, error: Exception, step: str):
        """
        Handle errors with appropriate recovery strategies
        """
        
        error_type = classify_error(error)
        strategy = RETRY_STRATEGIES.get(error_type, {})
        
        if should_retry(job_id, error_type, strategy):
            await schedule_retry(job_id, strategy)
        elif should_fallback(error_type):
            await try_fallback_strategy(job_id, error_type)
        else:
            await mark_job_failed(job_id, error, step)
```

---

## Error Handling Strategy

### Error Classification

```python
class ErrorClassification:
    """
    Categorizes errors for appropriate handling
    """
    
    TRANSIENT_ERRORS = [
        "NETWORK_TIMEOUT",
        "API_RATE_LIMIT", 
        "TEMPORARY_UNAVAILABLE",
        "CONNECTION_RESET"
    ]
    
    PERMANENT_ERRORS = [
        "VIDEO_NOT_FOUND",
        "VIDEO_PRIVATE",
        "INVALID_API_KEY",
        "INSUFFICIENT_CREDITS"
    ]
    
    RECOVERABLE_ERRORS = [
        "TRANSCRIPT_LANGUAGE_UNAVAILABLE",
        "PROVIDER_OVERLOADED",
        "PARTIAL_TRANSCRIPT_FAILURE"
    ]
```

### Error Response Handling

```python
class APIErrorHandler:
    """
    Handles API errors with proper HTTP status codes and user-friendly messages
    """
    
    ERROR_MAPPINGS = {
        # Client errors (4xx)
        "INVALID_URL": (400, "The provided YouTube URL is not valid"),
        "VIDEO_NOT_FOUND": (404, "Video not found or not accessible"),
        "TRANSCRIPT_UNAVAILABLE": (404, "No transcript available for this video"),
        "INVALID_LANGUAGE": (400, "Selected language is not available"),
        "INVALID_PROVIDER": (400, "Selected AI provider is not supported"),
        "JOB_NOT_FOUND": (404, "Job not found"),
        "JOB_ALREADY_CANCELLED": (409, "Job has already been cancelled"),
        
        # Server errors (5xx)
        "PROVIDER_ERROR": (502, "AI provider temporarily unavailable"),
        "PROCESSING_FAILED": (500, "Job processing failed unexpectedly"),
        "STORAGE_ERROR": (500, "Failed to save generated content"),
        "DATABASE_ERROR": (500, "Database operation failed"),
        
        # Rate limiting (429)
        "RATE_LIMIT_EXCEEDED": (429, "Too many requests, please try again later"),
        "QUOTA_EXCEEDED": (429, "API quota exceeded for selected provider")
    }
    
    async def handle_api_error(error: Exception, request_id: str) -> APIError:
        """
        Convert internal errors to user-friendly API responses
        """
        
        error_code = get_error_code(error)
        status_code, message = ERROR_MAPPINGS.get(
            error_code, 
            (500, "An unexpected error occurred")
        )
        
        return APIError(
            error=error_code,
            message=message,
            details=extract_error_details(error),
            request_id=request_id,
            timestamp=datetime.utcnow(),
            suggestions=get_error_suggestions(error_code)
        )
```

---

## Security Considerations

### API Security

```python
class SecurityConfig:
    """
    Security configuration and middleware
    """
    
    # Rate limiting
    RATE_LIMITS = {
        "video_validation": "10/minute",
        "job_creation": "5/minute", 
        "status_check": "60/minute",
        "websocket_connection": "3/minute"
    }
    
    # Input validation
    MAX_URL_LENGTH = 2048
    MAX_CUSTOM_PROMPT_LENGTH = 5000
    ALLOWED_FILE_EXTENSIONS = [".md", ".txt", ".html"]
    
    # CORS configuration
    CORS_ORIGINS = [
        "http://localhost:3000",  # Development
        "http://localhost:5173",  # Vite dev server
        # Production origins to be configured
    ]
    
    # API key handling
    API_KEY_PATTERNS = {
        "openai": r"^sk-[A-Za-z0-9]{48}$",
        "anthropic": r"^sk-ant-[A-Za-z0-9\-]{95}$",
        "google": r"^[A-Za-z0-9\-_]{39}$"
    }
```

### Data Protection

```python
class DataProtection:
    """
    Data protection and privacy controls
    """
    
    # Data retention policies
    RETENTION_POLICIES = {
        "completed_jobs": "30 days",
        "failed_jobs": "7 days", 
        "transcript_files": "24 hours",
        "output_files": "7 days",
        "websocket_logs": "24 hours"
    }
    
    # Data anonymization
    ANONYMIZE_FIELDS = [
        "client_ip",
        "user_agent", 
        "api_keys"
    ]
    
    # Secure file handling
    UPLOAD_RESTRICTIONS = {
        "max_file_size": "10MB",
        "allowed_mime_types": ["text/plain", "text/markdown"],
        "scan_for_malware": True
    }
```

---

## Performance Optimization

### Caching Strategy

```python
class CacheManager:
    """
    Multi-level caching for performance optimization
    """
    
    # Cache configuration
    CACHE_LEVELS = {
        "video_metadata": {
            "backend": "redis",
            "ttl": 3600,  # 1 hour
            "max_size": "100MB"
        },
        "transcript_languages": {
            "backend": "memory",
            "ttl": 1800,  # 30 minutes
            "max_entries": 1000
        },
        "provider_health": {
            "backend": "memory", 
            "ttl": 300,   # 5 minutes
            "max_entries": 10
        }
    }
    
    async def get_cached_video_info(video_id: str) -> Optional[VideoInfo]
    async def cache_video_info(video_id: str, info: VideoInfo)
    async def invalidate_cache(pattern: str)
```

### Database Optimization

```python
class DatabaseOptimization:
    """
    Database performance optimization strategies
    """
    
    # Connection pooling
    POOL_CONFIG = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600
    }
    
    # Query optimization
    INDEXES = [
        "idx_jobs_status_created",     # Composite index for job listing
        "idx_progress_job_step",       # Progress tracking queries
        "idx_ws_connections_active",   # Active WebSocket connections
        "idx_audit_timestamp"          # Audit log queries
    ]
    
    # Batch operations
    BATCH_SIZES = {
        "job_cleanup": 100,
        "progress_updates": 50,
        "audit_log_insert": 25
    }
```

### Async Processing Optimization

```python
class AsyncOptimization:
    """
    Async processing performance optimization
    """
    
    # Concurrency limits
    CONCURRENCY_LIMITS = {
        "max_concurrent_jobs": 5,
        "max_websocket_connections": 100,
        "max_database_connections": 20,
        "max_http_requests": 50
    }
    
    # Task scheduling
    TASK_PRIORITIES = {
        "job_processing": 1,      # Highest priority
        "websocket_updates": 2,   # Real-time updates
        "cache_cleanup": 3,       # Background maintenance
        "audit_logging": 4        # Lowest priority
    }
```

---

## Integration Points

### Existing CLI Module Integration

```python
class CLIIntegration:
    """
    Integration layer for existing CLI modules
    """
    
    # Module mappings
    MODULE_ADAPTERS = {
        "youtube_parser": "VideoService.parse_url",
        "transcript_handler": "VideoService.fetch_transcript", 
        "llm_providers": "ProviderService.generate_content",
        "blog_formatter": "ContentService.format_blog",
        "utils": "UtilityService.common_functions"
    }
    
    async def adapt_cli_function(module: str, function: str, **kwargs):
        """
        Adapt CLI functions for async web context
        """
        
        # Convert sync calls to async where needed
        # Add progress callbacks for long-running operations
        # Handle exceptions and convert to web-appropriate errors
        # Add logging and monitoring
```

### External API Integration

```python
class ExternalAPIIntegration:
    """
    Integration with external APIs and services
    """
    
    # API client configuration
    API_CLIENTS = {
        "youtube": {
            "base_url": "https://www.googleapis.com/youtube/v3",
            "timeout": 30,
            "retries": 3
        },
        "openai": {
            "timeout": 120,  # Longer timeout for generation
            "retries": 2
        },
        "anthropic": {
            "timeout": 120,
            "retries": 2
        }
    }
    
    # Health check endpoints
    HEALTH_CHECKS = {
        "youtube_api": "GET /youtube/v3/search",
        "openai_api": "GET /v1/models",
        "anthropic_api": "POST /v1/messages (test)",
        "google_ai": "GET /v1/models"
    }
```

### Monitoring and Observability

```python
class MonitoringIntegration:
    """
    Integration with monitoring and observability tools
    """
    
    # Metrics collection
    METRICS = {
        "job_processing_time": "histogram",
        "api_response_time": "histogram", 
        "websocket_connections": "gauge",
        "error_rate": "counter",
        "provider_success_rate": "gauge"
    }
    
    # Logging configuration
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "json",
        "fields": ["timestamp", "level", "message", "job_id", "request_id"],
        "rotation": "daily",
        "retention": "30 days"
    }
    
    # Health check endpoints
    HEALTH_ENDPOINTS = {
        "/health": "Basic health check",
        "/health/detailed": "Detailed system status",
        "/metrics": "Prometheus metrics",
        "/logs": "Recent log entries"
    }
```

---

This comprehensive backend design provides a solid foundation for implementing the FastAPI web interface while maintaining the robustness and functionality of the existing CLI application. The modular architecture ensures easy maintenance and future extensibility.
