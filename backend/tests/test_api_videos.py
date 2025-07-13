import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException

from main import app  # Changed from 'src.main' to 'main'
from src.services.video_service import VideoService


class TestVideosAPI:
    """Unit tests for Videos API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_video_info(self):
        """Mock video information response"""
        return {
            "video_id": "dQw4w9WgXcQ",
            "title": "Test Video Title",
            "author_name": "Test Channel",
            "author_url": "https://www.youtube.com/channel/UC123",
            "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
            "thumbnail_width": 1280,
            "thumbnail_height": 720,
            "fetched_at": "2024-01-01T12:00:00"
        }
    
    @patch('src.api.v1.videos.VideoService')
    def test_get_video_info_success(self, mock_video_service_class, client, mock_video_info):
        """Test successful video info retrieval"""
        mock_service = AsyncMock()
        mock_service.get_video_info.return_value = mock_video_info
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/dQw4w9WgXcQ/info")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Video Title"
        assert data["thumbnail"] == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
        assert data["duration"] == 0  # oEmbed doesn't provide duration
    
    @patch('src.api.v1.videos.VideoService')
    def test_get_video_info_invalid_id_format(self, mock_video_service_class, client):
        """Test video info with invalid video ID format"""
        response = client.get("/api/v1/videos/invalid/info")
        
        assert response.status_code == 400
        assert "Invalid video ID format" in response.json()["detail"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_get_video_info_not_found(self, mock_video_service_class, client):
        """Test video info for non-existent video"""
        mock_service = AsyncMock()
        mock_service.get_video_info.side_effect = ValueError("Video not found or private: test123")
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/invalid1234/info")
        
        assert response.status_code == 404
        assert "Video not found or private" in response.json()["detail"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_get_video_info_quota_exceeded(self, mock_video_service_class, client):
        """Test video info with quota exceeded error"""
        mock_service = AsyncMock()
        mock_service.get_video_info.side_effect = Exception("YouTube API quota exceeded")
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/dQw4w9WgXcQ/info")
        
        assert response.status_code == 429
        assert "quota exceeded" in response.json()["detail"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_get_video_info_network_error(self, mock_video_service_class, client):
        """Test video info with network error"""
        mock_service = AsyncMock()
        mock_service.get_video_info.side_effect = Exception("Network error while fetching video info")
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/dQw4w9WgXcQ/info")
        
        assert response.status_code == 503
        assert "Network error" in response.json()["detail"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_validate_video_success(self, mock_video_service_class, client):
        """Test successful video validation"""
        mock_validation_result = {
            "is_available": True,
            "video_info": {
                "video_id": "dQw4w9WgXcQ",
                "title": "Test Video",
                "author_name": "Test Channel",
                "thumbnail_url": "https://example.com/thumb.jpg"
            },
            "error": None
        }
        
        mock_service = AsyncMock()
        mock_service.validate_video_availability.return_value = mock_validation_result
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/dQw4w9WgXcQ/validate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["video_info"]["title"] == "Test Video"
        assert data["error_message"] is None
    
    @patch('src.api.v1.videos.VideoService')
    def test_validate_video_not_available(self, mock_video_service_class, client):
        """Test video validation for unavailable video"""
        mock_validation_result = {
            "is_available": False,
            "video_info": None,
            "error": "Video not found or private: test123"
        }
        
        mock_service = AsyncMock()
        mock_service.validate_video_availability.return_value = mock_validation_result
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/test1234567/validate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert data["video_info"] is None
        assert "Video not found or private" in data["error_message"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_validate_video_invalid_id(self, mock_video_service_class, client):
        """Test video validation with invalid video ID"""
        response = client.get("/api/v1/videos/short/validate")
        
        assert response.status_code == 400
        assert "Invalid video ID format" in response.json()["detail"]
    
    @patch('src.api.v1.videos.VideoService')
    def test_validate_video_service_error(self, mock_video_service_class, client):
        """Test video validation with service error"""
        mock_service = AsyncMock()
        mock_service.validate_video_availability.side_effect = Exception("Service error")
        mock_video_service_class.return_value = mock_service
        
        response = client.get("/api/v1/videos/dQw4w9WgXcQ/validate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert "Validation failed" in data["error_message"]
