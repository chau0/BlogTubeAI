"""Caching layer for performance optimization"""

import json
import asyncio
from typing import Any, Optional, Dict
from datetime import datetime, timedelta


class CacheManager:
    """In-memory cache manager with TTL support"""
    
    def __init__(self):
        self.cache: Dict[str, Dict] = {}
        self.ttl_config = {
            "video_metadata": 3600,  # 1 hour
            "transcript_languages": 1800,  # 30 minutes
            "provider_health": 300,  # 5 minutes
        }
    
    async def get(self, key: str, cache_type: str = "default") -> Optional[Any]:
        """Get cached value by key"""
        if key not in self.cache:
            return None
            
        cache_entry = self.cache[key]
        
        # Check if expired
        if datetime.now() > cache_entry["expires_at"]:
            del self.cache[key]
            return None
            
        return cache_entry["value"]
    
    async def set(self, key: str, value: Any, cache_type: str = "default",
                  ttl: Optional[int] = None) -> None:
        """Cache a value with TTL"""
        if ttl is None:
            ttl = self.ttl_config.get(cache_type, 3600)
            
        self.cache[key] = {
            "value": value,
            "expires_at": datetime.now() + timedelta(seconds=ttl),
            "cache_type": cache_type
        }
    
    async def delete(self, key: str) -> bool:
        """Delete cached value"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    async def clear_cache_type(self, cache_type: str) -> int:
        """Clear all cached values of a specific type"""
        keys_to_delete = [
            key for key, entry in self.cache.items()
            if entry.get("cache_type") == cache_type
        ]
        
        for key in keys_to_delete:
            del self.cache[key]
            
        return len(keys_to_delete)
    
    async def cleanup_expired(self) -> int:
        """Remove expired cache entries"""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now > entry["expires_at"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
            
        return len(expired_keys)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = len(self.cache)
        cache_types = {}
        
        for entry in self.cache.values():
            cache_type = entry.get("cache_type", "default")
            cache_types[cache_type] = cache_types.get(cache_type, 0) + 1
        
        return {
            "total_entries": total_entries,
            "types": cache_types,
            "memory_usage_mb": self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self) -> float:
        """Rough estimate of cache memory usage in MB"""
        total_size = 0
        for entry in self.cache.values():
            # Very rough estimation
            total_size += len(str(entry))
        return total_size / (1024 * 1024)