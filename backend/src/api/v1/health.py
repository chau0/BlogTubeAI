from fastapi import APIRouter
from datetime import datetime
from ...models.schemas import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="BlogTubeAI API is running",
        database="connected",
        version="1.0.0",
        uptime_seconds=0  # Will be calculated properly later
    )


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    return {"status": "ready", "timestamp": datetime.now().isoformat()}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive", "timestamp": datetime.now().isoformat()}
