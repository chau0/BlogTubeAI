import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import requests
from datetime import datetime

from src.services.video_service import VideoService


class TestVideoService:
    """Unit tests for VideoService"""
    
    @pytest.fixture
    def video_service(self):
        """Create VideoService instance for testing"""
        return VideoService()
    
    @pytest.fixture
    def mock_oembed_response(self):
        """Mock successful oEmbed API response"""
        return {
            "title": "Test Video Title",
            "author_name": "Test Channel",
            "author_url": "https://www.youtube.com/channel/UC123",
            "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
            "thumbnail_width": 1280,
            "thumbnail_height": 720,
            "html": "<iframe>...</iframe>",
            "width": 480,
            "height": 270,
            "provider_name": "YouTube",
            "provider_url": "https://www.youtube.com/",
            "type": "video",
            "version": "1.0"
        }
    
    def test_extract_video_id_standard_url(self, video_service):
        """Test video ID extraction from standard YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = video_service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_short_url(self, video_service):
        """Test video ID extraction from short YouTube URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = video_service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_embed_url(self, video_service):
        """Test video ID extraction from embed URL"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = video_service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self, video_service):
        """Test video ID extraction from invalid URL"""
        url = "https://www.example.com/video"
        video_id = video_service.extract_video_id(url)
        assert video_id is None
    
    def test_validate_youtube_url_valid(self, video_service):
        """Test YouTube URL validation with valid URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        is_valid = video_service.validate_youtube_url(url)
        assert is_valid is True
    
    def test_validate_youtube_url_invalid(self, video_service):
        """Test YouTube URL validation with invalid URL"""
        url = "https://www.example.com/video"
        is_valid = video_service.validate_youtube_url(url)
        assert is_valid is False
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_get_video_info_success(self, mock_get, video_service, mock_oembed_response):
        """Test successful video info retrieval"""
        # Mock cache miss
        video_service.cache_manager.get = AsyncMock(return_value=None)
        video_service.cache_manager.set = AsyncMock()
        
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_oembed_response
        mock_get.return_value = mock_response
        
        video_id = "dQw4w9WgXcQ"
        result = await video_service.get_video_info(video_id)
        
        assert result["video_id"] == video_id
        assert result["title"] == "Test Video Title"
        assert result["author_name"] == "Test Channel"
        assert result["thumbnail_url"] == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        assert "fetched_at" in result
        
        # Verify cache was called
        video_service.cache_manager.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_video_info_from_cache(self, video_service):
        """Test video info retrieval from cache"""
        cached_data = {
            "video_id": "dQw4w9WgXcQ",
            "title": "Cached Video Title",
            "author_name": "Cached Channel"
        }
        
        video_service.cache_manager.get = AsyncMock(return_value=cached_data)
        
        result = await video_service.get_video_info("dQw4w9WgXcQ")
        
        assert result == cached_data
        video_service.cache_manager.get.assert_called_once()
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_get_video_info_not_found(self, mock_get, video_service):
        """Test video info retrieval for non-existent video"""
        video_service.cache_manager.get = AsyncMock(return_value=None)
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Video not found or private"):
            await video_service.get_video_info("invalid123")
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_get_video_info_region_restricted(self, mock_get, video_service):
        """Test video info retrieval for region-restricted video"""
        video_service.cache_manager.get = AsyncMock(return_value=None)
        
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Video not available in this region"):
            await video_service.get_video_info("restricted123")
    
    @patch('requests.get')
    @pytest.mark.asyncio
    async def test_get_video_info_network_error(self, mock_get, video_service):
        """Test video info retrieval with network error"""
        video_service.cache_manager.get = AsyncMock(return_value=None)
        
        mock_get.side_effect = requests.RequestException("Connection timeout")
        
        with pytest.raises(Exception, match="Network error while fetching video info"):
            await video_service.get_video_info("dQw4w9WgXcQ")
    
    @pytest.mark.asyncio
    async def test_validate_video_availability_success(self, video_service):
        """Test video availability validation for available video"""
        mock_video_info = {
            "video_id": "dQw4w9WgXcQ",
            "title": "Test Video",
            "author_name": "Test Channel"
        }
        
        video_service.get_video_info = AsyncMock(return_value=mock_video_info)
        
        result = await video_service.validate_video_availability("dQw4w9WgXcQ")
        
        assert result["is_available"] is True
        assert result["video_info"] == mock_video_info
        assert result["error"] is None
    
    @pytest.mark.asyncio
    async def test_validate_video_availability_not_found(self, video_service):
        """Test video availability validation for non-existent video"""
        video_service.get_video_info = AsyncMock(
            side_effect=ValueError("Video not found or private: invalid123")
        )
        
        result = await video_service.validate_video_availability("invalid123")
        
        assert result["is_available"] is False
        assert result["video_info"] is None
        assert "Video not found or private" in result["error"]
    
    @pytest.mark.asyncio
    async def test_validate_video_availability_service_error(self, video_service):
        """Test video availability validation with service error"""
        video_service.get_video_info = AsyncMock(
            side_effect=Exception("YouTube API quota exceeded")
        )
        
        result = await video_service.validate_video_availability("dQw4w9WgXcQ")
        
        assert result["is_available"] is False
        assert result["video_info"] is None
        assert "Service temporarily unavailable" in result["error"]
    
    def test_format_video_info(self, video_service, mock_oembed_response):
        """Test video info formatting"""
        video_id = "dQw4w9WgXcQ"
        result = video_service._format_video_info(mock_oembed_response, video_id)
        
        assert result["video_id"] == video_id
        assert result["title"] == mock_oembed_response["title"]
        assert result["author_name"] == mock_oembed_response["author_name"]
        assert result["thumbnail_url"] == mock_oembed_response["thumbnail_url"]
        assert "fetched_at" in result
        assert isinstance(result["fetched_at"], str)
    
    def test_handle_video_info_error_not_found(self, video_service):
        """Test error handling for not found errors"""
        error = ValueError("Video not found")
        result = video_service._handle_video_info_error(error, "test123")
        
        assert isinstance(result, ValueError)
        assert "Video not found or private" in str(result)
    
    def test_handle_video_info_error_region_restricted(self, video_service):
        """Test error handling for region restriction errors"""
        error = Exception("Video not available in this region")
        result = video_service._handle_video_info_error(error, "test123")
        
        assert isinstance(result, ValueError)
        assert "Video not available in this region" in str(result)
    
    def test_handle_video_info_error_quota_exceeded(self, video_service):
        """Test error handling for quota exceeded errors"""
        error = Exception("YouTube API quota exceeded")
        result = video_service._handle_video_info_error(error, "test123")
        
        assert isinstance(result, Exception)
        assert "quota exceeded" in str(result)
    
    def test_handle_video_info_error_network(self, video_service):
        """Test error handling for network errors"""
        error = Exception("Network timeout occurred")
        result = video_service._handle_video_info_error(error, "test123")
        
        assert isinstance(result, Exception)
        assert "Network error" in str(result)
    
    def test_parse_youtube_url_with_timestamp(self, video_service):
        """Test YouTube URL parsing with timestamp parameter"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120s"
        result = video_service.parse_youtube_url(url)
        
        assert result["video_id"] == "dQw4w9WgXcQ"
        assert result["timestamp"] == "120s"
        assert result["original_url"] == url
    
    def test_parse_youtube_url_with_playlist(self, video_service):
        """Test YouTube URL parsing with playlist parameter"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLtest123"
        result = video_service.parse_youtube_url(url)
        
        assert result["video_id"] == "dQw4w9WgXcQ"
        assert result["playlist_id"] == "PLtest123"
        assert result["original_url"] == url
