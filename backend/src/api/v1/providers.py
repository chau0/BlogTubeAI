from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.schemas import ProviderInfo
from ...services.provider_service import ProviderService

router = APIRouter()


@router.get("/", response_model=List[ProviderInfo])
async def list_providers():
    """List available LLM providers"""
    provider_service = ProviderService()
    providers = await provider_service.get_all_providers()
    
    return providers


@router.get("/{provider_name}/models")
async def list_provider_models(provider_name: str):
    """List available models for a provider"""
    provider_service = ProviderService()
    
    try:
        models = await provider_service.get_provider_models(provider_name)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{provider_name}/test")
async def test_provider_connection(provider_name: str):
    """Test connection to LLM provider"""
    provider_service = ProviderService()
    
    try:
        result = await provider_service.test_provider_connection(provider_name)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
