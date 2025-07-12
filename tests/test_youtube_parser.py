"""
Unit tests for YouTube URL Parser (F01)
"""

import pytest
from unittest.mock import patch, Mock
from src.youtube_parser import get_video_id, get_video_title, get_video_info


class TestGetVideoId:
    """Test video ID extraction from various URL formats."""
    
    def test_standard_watch_url(self):
        """Test standard YouTube watch URL."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert get_video_id(url) == "dQw4w9WgXcQ"
    
    def test_short_url(self):
        """Test youtu.be short URL format."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert get_video_id(url) == "dQw4w9WgXcQ"
    
    def test_embed_url(self):
        """Test embed URL format."""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert get_video_id(url) == "dQw4w9WgXcQ"
    
    def test_old_v_format(self):
        """Test old /v/ URL format."""
        url = "https://www.youtube.com/v/dQw4w9WgXcQ"
        assert get_video_id(url) == "dQw4w9WgXcQ"
    
    def test_invalid_url(self):
        """Test invalid URLs return None."""
        assert get_video_id("https://example.com") is None
        assert get_video_id("not-a-url") is None
        assert get_video_id("") is None
    
    def test_invalid_video_id_length(self):
        """Test URLs with invalid video ID length."""
        url = "https://www.youtube.com/watch?v=short"
        assert get_video_id(url) is None


class TestGetVideoTitle:
    """Test video title fetching."""
    
    @patch('src.youtube_parser.requests.get')
    def test_successful_title_fetch(self, mock_get):
        """Test successful title fetch from oEmbed API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"title": "Test Video Title"}
        mock_get.return_value = mock_response
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "Test Video Title"
    
    @patch('src.youtube_parser.requests.get')
    def test_failed_title_fetch(self, mock_get):
        """Test fallback when title fetch fails."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "YouTube Video dQw4w9WgXcQ"
    
    @patch('src.youtube_parser.requests.get')
    def test_exception_handling(self, mock_get):
        """Test exception handling in title fetch."""
        mock_get.side_effect = Exception("Network error")
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "YouTube Video dQw4w9WgXcQ"


class TestGetVideoInfo:
    """Test comprehensive video info fetching."""
    
    @patch('src.youtube_parser.requests.get')
    def test_successful_info_fetch(self, mock_get):
        """Test successful video info fetch."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "title": "Test Video",
            "author_name": "Test Channel"
        }
        mock_get.return_value = mock_response
        
        info = get_video_info("dQw4w9WgXcQ")
        assert info["title"] == "Test Video"
        assert info["author_name"] == "Test Channel"
    
    @patch('src.youtube_parser.requests.get')
    def test_failed_info_fetch(self, mock_get):
        """Test fallback when info fetch fails."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        info = get_video_info("dQw4w9WgXcQ")
        assert info["title"] == "YouTube Video dQw4w9WgXcQ"
        assert info["author_name"] == "Unknown"
