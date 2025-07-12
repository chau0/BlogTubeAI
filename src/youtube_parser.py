"""
YouTube URL Parser and Video Information Extractor
"""

import re
import requests
from urllib.parse import urlparse, parse_qs
from typing import Optional

def get_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    
    Args:
        url (str): YouTube URL
        
    Returns:
        Optional[str]: Video ID if found, None otherwise
    """
    # Pattern for video ID (11 characters, alphanumeric + underscores/hyphens)
    video_id_pattern = r'[a-zA-Z0-9_-]{11}'
    
    # Parse URL
    parsed_url = urlparse(url)
    
    # Standard watch URL
    if 'youtube.com' in parsed_url.netloc and 'watch' in parsed_url.path:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            video_id = query_params['v'][0]
            if re.match(video_id_pattern, video_id):
                return video_id
    
    # Short URL format (youtu.be)
    elif 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.lstrip('/')
        if re.match(video_id_pattern, video_id):
            return video_id
    
    # Embed URL format
    elif 'youtube.com' in parsed_url.netloc and 'embed' in parsed_url.path:
        video_id = parsed_url.path.split('/')[-1]
        if re.match(video_id_pattern, video_id):
            return video_id
    
    # Old format /v/VIDEO_ID
    elif 'youtube.com' in parsed_url.netloc and '/v/' in parsed_url.path:
        video_id = parsed_url.path.split('/v/')[-1].split('?')[0]
        if re.match(video_id_pattern, video_id):
            return video_id
    
    return None

def get_video_title(video_id: str) -> str:
    """
    Get video title from YouTube video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Video title or placeholder if not found
    """
    try:
        # Use YouTube oEmbed API to get video info
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('title', f'YouTube Video {video_id}')
        else:
            return f'YouTube Video {video_id}'
            
    except Exception:
        return f'YouTube Video {video_id}'

def get_video_info(video_id: str) -> dict:
    """
    Get comprehensive video information.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Video information including title, author, etc.
    """
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'title': f'YouTube Video {video_id}', 'author_name': 'Unknown'}
            
    except Exception:
        return {'title': f'YouTube Video {video_id}', 'author_name': 'Unknown'}
