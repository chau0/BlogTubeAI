from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import asyncio
from datetime import datetime

from .config import get_settings
from .middleware.cors import setup_cors
from .middleware.rate_limit import setup_rate_limiting
from .middleware.logging import setup_logging
from ..api.v1.router import api_router
from ..api.websocket.handlers import websocket_router
from ..database.connection import init_db
from ..models.schemas import APIError


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title="BlogTubeAI API",
        description="Transform YouTube videos into engaging blog posts",
        version="1.0.0",
        docs_url="/api/docs" if settings.environment != "production" else None,
        redoc_url="/api/redoc" if settings.environment != "production" else None,
    )
    
    # Setup middleware
    setup_cors(app)
    setup_rate_limiting(app) 
    setup_logging(app)
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(websocket_router, prefix="/ws")
    
    # Serve static files in production
    if os.path.exists("static/frontend"):
        app.mount("/", StaticFiles(directory="static/frontend", html=True), name="frontend")
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions"""
        error_response = APIError(
            error="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details={"exception_type": type(exc).__name__},
            request_id=str(id(request)),
            timestamp=datetime.now(),
            suggestions=["Please try again later", "Contact support if the issue persists"]
        )
        
        return JSONResponse(
            status_code=500,
            content=error_response.dict()
        )
    
    # Application lifecycle events
    @app.on_event("startup")
    async def startup_event():
        """Initialize application on startup"""
        await init_db()
        
        # Start background cleanup tasks
        asyncio.create_task(start_background_tasks())
    
    @app.on_event("shutdown") 
    async def shutdown_event():
        """Cleanup on application shutdown"""
        # Perform cleanup tasks
        pass
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Basic health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    
    return app


async def start_background_tasks():
    """Start background maintenance tasks"""
    from ..core.job_manager import JobManager
    from ..api.websocket.manager import websocket_manager
    from ..core.file_manager import FileManager
    from ..core.cache_manager import CacheManager
    
    job_manager = JobManager()
    file_manager = FileManager()
    cache_manager = CacheManager()
    
    while True:
        try:
            # Clean up stale WebSocket connections every 5 minutes
            await websocket_manager.cleanup_stale_connections()
            
            # Clean up expired cache entries every 10 minutes
            await cache_manager.cleanup_expired()
            
            # Clean up temporary files every hour
            file_manager.cleanup_temp_files()
            
            # Clean up completed jobs every 6 hours  
            await job_manager.cleanup_completed_jobs()
            
            # Wait 5 minutes before next cleanup cycle
            await asyncio.sleep(300)
            
        except Exception as e:
            # Log error but don't crash the background task
            print(f"Background task error: {e}")
            await asyncio.sleep(300)
