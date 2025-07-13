from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from .config import get_settings
from .middleware.cors import setup_cors
from .middleware.rate_limit import setup_rate_limiting
from .middleware.logging import setup_logging
from ..api.v1.router import api_router
from ..api.websocket.handlers import websocket_router
from ..database.connection import init_db


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
    
    # Initialize database
    @app.on_event("startup")
    async def startup_event():
        await init_db()
    
    return app
