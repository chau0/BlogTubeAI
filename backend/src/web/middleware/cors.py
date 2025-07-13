from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..config import get_settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware"""
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
