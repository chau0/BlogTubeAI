from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database.connection import get_db
from ...models.schemas import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="BlogTubeAI API is running",
        database="connected"
    )


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}
