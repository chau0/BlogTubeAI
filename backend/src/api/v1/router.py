from fastapi import APIRouter

from .videos import router as videos_router
from .jobs import router as jobs_router
from .providers import router as providers_router
from .health import router as health_router

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(videos_router, prefix="/videos", tags=["videos"])
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
api_router.include_router(providers_router, prefix="/providers", tags=["providers"])
