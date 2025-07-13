"""
Utility Functions
Common utilities for the YouTube to Blog converter.
"""

import re
import os
from urllib.parse import urlparse
from typing import Optional

def validate_url(url: str) -> bool:
    """
    Validate if URL is a valid YouTube URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid YouTube URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        parsed = urlparse(url)
        
        # Check for valid protocol
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for YouTube domains
        valid_domains = [
            'youtube.com', 'www.youtube.com',
            'youtu.be', 'www.youtu.be',
            'm.youtube.com'
        ]
        
        return any(domain in parsed.netloc for domain in valid_domains)
        
    except Exception:
        return False

def create_safe_filename(title: str, max_length: int = 50) -> str:
    """
    Create a safe filename from video title.
    
    Args:
        title (str): Video title
        max_length (int): Maximum filename length
        
    Returns:
        str: Safe filename
    """
    if not title:
        return "youtube_blog"
    
    # Remove invalid characters
    safe_title = re.sub(r'[^\w\s-]', '', title)
    
    # Replace spaces with underscores
    safe_title = re.sub(r'\s+', '_', safe_title)
    
    # Remove multiple underscores
    safe_title = re.sub(r'_+', '_', safe_title)
    
    # Trim length
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length]
    
    # Remove trailing underscores
    safe_title = safe_title.strip('_')
    
    return safe_title.lower() or "youtube_blog"

def ensure_directory_exists(path: str) -> bool:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path (str): Directory path
        
    Returns:
        bool: True if directory exists or was created
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception:
        return False

def get_file_size(filepath: str) -> Optional[int]:
    """
    Get file size in bytes.
    
    Args:
        filepath (str): Path to file
        
    Returns:
        Optional[int]: File size in bytes or None if error
    """
    try:
        return os.path.getsize(filepath)
    except Exception:
        return None

def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def clean_text(text: str) -> str:
    """
    Cleans the given transcript text by removing artifacts like [Music], [Applause],
    handling None input, and fixing punctuation spacing.
    
    Args:
        text (str): The transcript text to clean.
    
    Returns:
        str: The cleaned transcript text.
    """
    if text is None:
        return ""
    
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Remove artifacts like [Music], [Applause], [Laughter] along with surrounding spaces
    text = re.sub(r'\s*\[.*?\]\s*', ' ', text)
    
    # Remove extra spaces and newlines
    text = ' '.join(text.split())
    
    # Fix punctuation spacing
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r'\s+\?', '?', text)
    text = re.sub(r'\s+!', '!', text)
    
    return text