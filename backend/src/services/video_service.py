"""Video processing service"""

import re
from typing import Optional, List, Dict
from urllib.parse import urlparse, parse_qs

from ..core.cache_manager import CacheManager


class VideoService:
    """Service for video-related operations"""
    
    def __init__(self):
        self.cache_manager = CacheManager()
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        # Regular expressions for different YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def validate_youtube_url(self, url: str) -> bool:
        """Validate if URL is a valid YouTube URL"""
        return self.extract_video_id(url) is not None
    
    async def get_cached_video_info(self, video_id: str) -> Optional[Dict]:
        """Get cached video information"""
        cache_key = f"video_info:{video_id}"
        return await self.cache_manager.get(cache_key, "video_metadata")
    
    async def cache_video_info(self, video_id: str, info: Dict) -> None:
        """Cache video information"""
        cache_key = f"video_info:{video_id}"
        await self.cache_manager.set(cache_key, info, "video_metadata")
    
    def parse_youtube_url(self, url: str) -> Dict[str, str]:
        """Parse YouTube URL and extract components"""
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        result = {
            "original_url": url,
            "domain": parsed.netloc,
            "path": parsed.path,
            "video_id": self.extract_video_id(url)
        }
        
        # Extract additional parameters
        if "t" in query_params:
            result["timestamp"] = query_params["t"][0]
        if "list" in query_params:
            result["playlist_id"] = query_params["list"][0]
        
        return result