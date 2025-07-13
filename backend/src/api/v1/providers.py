from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...models.schemas import ProviderResponse, ProviderConfig
from ...services.provider_service import ProviderService

router = APIRouter()


@router.get("/", response_model=List[ProviderResponse])
async def list_providers():
    """List available LLM providers"""
    provider_service = ProviderService()
    providers = provider_service.get_available_providers()
    
    return [ProviderResponse(**provider) for provider in providers]


@router.get("/{provider_name}/models")
async def list_provider_models(provider_name: str):
    """List available models for a provider"""
    provider_service = ProviderService()
    
    try:
        models = provider_service.get_provider_models(provider_name)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{provider_name}/test")
async def test_provider_connection(provider_name: str, config: ProviderConfig):
    """Test connection to LLM provider"""
    provider_service = ProviderService()
    
    try:
        result = provider_service.test_connection(provider_name, config.dict())
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
