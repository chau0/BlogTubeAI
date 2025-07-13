"""Video processing service"""

import re
from typing import Optional, List, Dict
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime

from ..core.cache_manager import CacheManager
from ..core.youtube_parser import get_video_info


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
    
    async def get_video_info(self, video_id: str) -> Dict:
        """Get comprehensive video information with caching"""
        # Check cache first
        cached_info = await self.get_cached_video_info(video_id)
        if cached_info:
            return cached_info
        
        try:
            # Get video info from YouTube oEmbed API
            video_info = self._fetch_video_metadata(video_id)
            
            # Cache the result
            await self.cache_video_info(video_id, video_info)
            
            return video_info
            
        except Exception as e:
            raise self._handle_video_info_error(e, video_id)
    
    def _fetch_video_metadata(self, video_id: str) -> Dict:
        """Fetch video metadata from YouTube API"""
        try:
            # Use YouTube oEmbed API
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(oembed_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_video_info(data, video_id)
            elif response.status_code == 404:
                raise ValueError(f"Video not found or private: {video_id}")
            elif response.status_code == 403:
                raise ValueError(f"Video not available in this region: {video_id}")
            else:
                raise Exception(f"YouTube API error: {response.status_code}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error while fetching video info: {str(e)}")
    
    def _format_video_info(self, oembed_data: Dict, video_id: str) -> Dict:
        """Format video information for consistent API response"""
        return {
            "video_id": video_id,
            "title": oembed_data.get("title", "Unknown Title"),
            "author_name": oembed_data.get("author_name", "Unknown Channel"),
            "author_url": oembed_data.get("author_url"),
            "thumbnail_url": oembed_data.get("thumbnail_url"),
            "thumbnail_width": oembed_data.get("thumbnail_width"),
            "thumbnail_height": oembed_data.get("thumbnail_height"),
            "html": oembed_data.get("html"),
            "width": oembed_data.get("width"),
            "height": oembed_data.get("height"),
            "provider_name": oembed_data.get("provider_name", "YouTube"),
            "provider_url": oembed_data.get("provider_url", "https://www.youtube.com/"),
            "type": oembed_data.get("type", "video"),
            "version": oembed_data.get("version", "1.0"),
            "fetched_at": datetime.utcnow().isoformat()
        }
    
    def _handle_video_info_error(self, error: Exception, video_id: str) -> Exception:
        """Handle and categorize video info errors"""
        error_msg = str(error).lower()
        
        if "not found" in error_msg or "private" in error_msg:
            return ValueError(f"Video not found or private: {video_id}")
        elif "region" in error_msg or "not available" in error_msg:
            return ValueError(f"Video not available in this region: {video_id}")
        elif "quota" in error_msg or "rate limit" in error_msg:
            return Exception(f"YouTube API quota exceeded. Please try again later.")
        elif "network" in error_msg or "timeout" in error_msg:
            return Exception(f"Network error while fetching video information")
        else:
            return Exception(f"Failed to fetch video information: {str(error)}")
    
    async def validate_video_availability(self, video_id: str) -> Dict[str, any]:
        """Validate video availability and return status info"""
        try:
            video_info = await self.get_video_info(video_id)
            return {
                "is_available": True,
                "video_info": video_info,
                "error": None
            }
        except ValueError as e:
            return {
                "is_available": False,
                "video_info": None,
                "error": str(e)
            }
        except Exception as e:
            return {
                "is_available": False,
                "video_info": None,
                "error": f"Service temporarily unavailable: {str(e)}"
            }