from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API
    api_host: str = "localhost"
    api_port: int = 8000
    api_workers: int = 1
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./blogtube.db"
    database_echo: bool = False
    
    # Redis (for caching and WebSocket - optional)
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Job Processing
    max_concurrent_jobs: int = 5
    job_timeout_minutes: int = 30
    
    # File Storage
    output_directory: str = "output"
    transcript_directory: str = "transcripts"
    temp_directory: str = "temp"
    
    # LLM API Keys (optional)
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    
    model_config = {"env_file": ".env"}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
