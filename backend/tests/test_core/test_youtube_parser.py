"""
Unit tests for YouTube URL Parser (F01)
"""

import pytest
from unittest.mock import patch, Mock
from src.core.youtube_parser import get_video_id, get_video_title, get_video_info


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
    
    def test_playlist_url(self):
        """Test URL with playlist parameter."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLyAiZRD-Bs9LMDo0e-y1t-X9Fy9oXNLhJ"
        assert get_video_id(url) == "dQw4w9WgXcQ"
    
    def test_invalid_url(self):
        """Test invalid YouTube URL."""
        url = "https://www.google.com"
        assert get_video_id(url) is None
    
    def test_empty_url(self):
        """Test empty URL."""
        assert get_video_id("") is None


class TestGetVideoTitle:
    """Test video title extraction."""
    
    @patch('src.core.youtube_parser.requests.get')
    def test_successful_title_fetch(self, mock_get):
        """Test successful title extraction."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test Video Title',
            'author_name': 'Test Author'
        }
        mock_get.return_value = mock_response
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "Test Video Title"
        
        expected_url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&format=json"
        mock_get.assert_called_once_with(expected_url, timeout=10)
    
    @patch('src.core.youtube_parser.requests.get')
    def test_failed_title_fetch(self, mock_get):
        """Test failed title extraction."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "YouTube Video dQw4w9WgXcQ"
    
    @patch('src.core.youtube_parser.requests.get')
    def test_exception_handling(self, mock_get):
        """Test exception handling during title fetch."""
        mock_get.side_effect = Exception("Network error")
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "YouTube Video dQw4w9WgXcQ"
    
    @patch('src.core.youtube_parser.requests.get')
    def test_missing_title_in_response(self, mock_get):
        """Test handling when title is missing from API response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'author_name': 'Test Author'
            # title key is missing
        }
        mock_get.return_value = mock_response
        
        title = get_video_title("dQw4w9WgXcQ")
        assert title == "YouTube Video dQw4w9WgXcQ"


class TestGetVideoInfo:
    """Test video information extraction."""
    
    @patch('src.core.youtube_parser.requests.get')
    def test_successful_info_fetch(self, mock_get):
        """Test successful video info extraction."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'title': 'Test Video Title',
            'author_name': 'Test Author',
            'thumbnail_url': 'https://example.com/thumb.jpg'
        }
        mock_get.return_value = mock_response
        
        info = get_video_info("dQw4w9WgXcQ")
        
        assert info['title'] == "Test Video Title"
        assert info['author_name'] == "Test Author"
        assert info['thumbnail_url'] == "https://example.com/thumb.jpg"
        
        expected_url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&format=json"
        mock_get.assert_called_once_with(expected_url, timeout=10)
    
    @patch('src.core.youtube_parser.requests.get')
    def test_failed_info_fetch(self, mock_get):
        """Test failed video info extraction."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        info = get_video_info("dQw4w9WgXcQ")
        
        assert info['title'] == "YouTube Video dQw4w9WgXcQ"
        assert info['author_name'] == "Unknown"
    
    @patch('src.core.youtube_parser.requests.get')
    def test_exception_handling_info(self, mock_get):
        """Test exception handling during info fetch."""
        mock_get.side_effect = Exception("Network error")
        
        info = get_video_info("dQw4w9WgXcQ")
        
        assert info['title'] == "YouTube Video dQw4w9WgXcQ"
        assert info['author_name'] == "Unknown"
