"""LLM provider management service"""

from typing import Dict, List, Optional
from datetime import datetime

from ..core.cache_manager import CacheManager
from ..models.schemas import ProviderInfo
from ..models.enums import LLMProvider


class ProviderService:
    """Service for managing LLM providers"""
    
    def __init__(self):
        self.cache_manager = CacheManager()
        self.providers_config = {
            LLMProvider.OPENAI: {
                "display_name": "OpenAI",
                "description": "GPT models from OpenAI",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                "features": ["chat", "completion", "function_calling"],
                "pricing_tier": "premium",
                "rate_limits": {"requests_per_minute": 60, "tokens_per_minute": 40000}
            },
            LLMProvider.ANTHROPIC: {
                "display_name": "Anthropic",
                "description": "Claude models from Anthropic",
                "models": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
                "features": ["chat", "completion", "long_context"],
                "pricing_tier": "premium",
                "rate_limits": {"requests_per_minute": 60, "tokens_per_minute": 40000}
            },
            LLMProvider.GOOGLE: {
                "display_name": "Google AI",
                "description": "Gemini models from Google",
                "models": ["gemini-pro", "gemini-pro-vision"],
                "features": ["chat", "completion", "multimodal"],
                "pricing_tier": "standard",
                "rate_limits": {"requests_per_minute": 60, "tokens_per_minute": 32000}
            }
        }
    
    async def get_all_providers(self) -> List[ProviderInfo]:
        """Get information about all available providers"""
        providers = []
        
        for provider_enum, config in self.providers_config.items():
            # Check cached health status
            health_status = await self._get_provider_health(provider_enum.value)
            
            provider_info = ProviderInfo(
                name=provider_enum.value,
                display_name=config["display_name"],
                description=config["description"],
                models=config["models"],
                is_available=health_status.get("is_available", False),
                features=config["features"],
                pricing_tier=config["pricing_tier"],
                rate_limits=config["rate_limits"],
                last_health_check=health_status.get("last_check")
            )
            providers.append(provider_info)
        
        return providers
    
    async def get_provider(self, provider_name: str) -> Optional[ProviderInfo]:
        """Get information about a specific provider"""
        if provider_name not in [p.value for p in LLMProvider]:
            return None
        
        config = self.providers_config.get(LLMProvider(provider_name))
        if not config:
            return None
        
        health_status = await self._get_provider_health(provider_name)
        
        return ProviderInfo(
            name=provider_name,
            display_name=config["display_name"],
            description=config["description"],
            models=config["models"],
            is_available=health_status.get("is_available", False),
            features=config["features"],
            pricing_tier=config["pricing_tier"],
            rate_limits=config["rate_limits"],
            last_health_check=health_status.get("last_check")
        )
    
    async def validate_provider_config(self, provider_name: str, 
                                     api_key: str, model: Optional[str] = None) -> Dict:
        """Validate provider configuration and credentials"""
        # This would implement actual API key validation
        # For now, return a mock response
        return {
            "is_valid": True,
            "provider": provider_name,
            "model": model,
            "capabilities": ["text_generation", "chat_completion"],
            "quota_info": {
                "remaining_requests": 1000,
                "reset_time": datetime.now().isoformat()
            }
        }
    
    async def check_provider_health(self, provider_name: str) -> Dict:
        """Check provider health and availability"""
        # This would implement actual health checking
        # For now, return a mock response
        health_data = {
            "is_available": True,
            "response_time_ms": 150,
            "last_check": datetime.now(),
            "error_message": None
        }
        
        # Cache the health status
        cache_key = f"provider_health:{provider_name}"
        await self.cache_manager.set(cache_key, health_data, "provider_health")
        
        return health_data
    
    async def _get_provider_health(self, provider_name: str) -> Dict:
        """Get cached provider health status"""
        cache_key = f"provider_health:{provider_name}"
        cached_health = await self.cache_manager.get(cache_key, "provider_health")
        
        if cached_health:
            return cached_health
        
        # If not cached, perform health check
        return await self.check_provider_health(provider_name)
    
    def get_provider_models(self, provider_name: str) -> List[str]:
        """Get available models for a provider"""
        config = self.providers_config.get(LLMProvider(provider_name))
        return config["models"] if config else []
    
    def is_provider_supported(self, provider_name: str) -> bool:
        """Check if provider is supported"""
        return provider_name in [p.value for p in LLMProvider]