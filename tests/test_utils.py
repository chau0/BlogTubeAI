"""
Unit tests for Utilities (F07, F08)
"""

import pytest
import tempfile
import os
from src.utils import validate_url, create_safe_filename, ensure_directory_exists, get_file_size, truncate_text, clean_text


class TestValidateUrl:
    """Test F07/F08: URL validation for CLI interaction and error handling."""
    
    def test_valid_youtube_urls(self):
        """Test validation of valid YouTube URLs."""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        for url in valid_urls:
            assert validate_url(url) is True
    
    def test_invalid_urls(self):
        """Test rejection of invalid URLs."""
        invalid_urls = [
            "https://example.com",
            "not-a-url",
            "",
            None,
            123,
            "https://vimeo.com/123456"
        ]
        
        for url in invalid_urls:
            assert validate_url(url) is False
    
    def test_malformed_urls(self):
        """Test handling of malformed URLs."""
        malformed_urls = [
            "youtube.com",  # Missing protocol
            "https://",     # Incomplete URL
            "ftp://youtube.com/watch?v=test"  # Wrong protocol
        ]
        
        for url in malformed_urls:
            assert validate_url(url) is False


class TestCreateSafeFilename:
    """Test safe filename creation for file operations."""
    
    def test_basic_filename_creation(self):
        """Test basic safe filename creation."""
        title = "My Awesome Video Title"
        filename = create_safe_filename(title)
        assert filename == "my_awesome_video_title"
    
    def test_remove_invalid_characters(self):
        """Test removal of invalid filename characters."""
        title = "Video: Title with/Invalid\\Characters*?"
        filename = create_safe_filename(title)
        assert "/" not in filename
        assert "\\" not in filename
        assert "*" not in filename
        assert "?" not in filename
        assert ":" not in filename
    
    def test_length_truncation(self):
        """Test filename length truncation."""
        long_title = "A" * 100
        filename = create_safe_filename(long_title, max_length=20)
        assert len(filename) <= 20
    
    def test_empty_title_fallback(self):
        """Test fallback for empty titles."""
        assert create_safe_filename("") == "youtube_blog"
        assert create_safe_filename(None) == "youtube_blog"
    
    def test_multiple_spaces_handling(self):
        """Test handling of multiple spaces."""
        title = "Video    with     multiple    spaces"
        filename = create_safe_filename(title)
        assert "  " not in filename
        assert filename == "video_with_multiple_spaces"


class TestEnsureDirectoryExists:
    """Test directory creation utilities."""
    
    def test_create_new_directory(self):
        """Test creation of new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_test_dir")
            
            result = ensure_directory_exists(new_dir)
            
            assert result is True
            assert os.path.exists(new_dir)
            assert os.path.isdir(new_dir)
    
    def test_existing_directory(self):
        """Test handling of existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = ensure_directory_exists(temp_dir)
            assert result is True
    
    def test_invalid_path(self):
        """Test handling of invalid paths."""
        # Test with a path that would cause permission error
        invalid_path = "/root/test_dir" if os.name != 'nt' else "C:\\Windows\\System32\\test_dir"
        result = ensure_directory_exists(invalid_path)
        # Should return False due to permission error
        assert result is False


class TestGetFileSize:
    """Test file size utilities."""
    
    def test_existing_file_size(self):
        """Test getting size of existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            size = get_file_size(temp_path)
            assert size is not None
            assert size > 0
        finally:
            os.unlink(temp_path)
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent file."""
        size = get_file_size("/nonexistent/file.txt")
        assert size is None


class TestTruncateText:
    """Test text truncation utilities."""
    
    def test_no_truncation_needed(self):
        """Test when text is shorter than max length."""
        text = "Short text"
        result = truncate_text(text, 100)
        assert result == text
    
    def test_truncation_with_ellipsis(self):
        """Test text truncation with ellipsis."""
        text = "A" * 100
        result = truncate_text(text, 20)
        assert len(result) == 20
        assert result.endswith("...")
    
    def test_empty_text(self):
        """Test handling of empty text."""
        assert truncate_text("", 100) == ""
        assert truncate_text(None, 100) is None


class TestCleanText:
    """Test text cleaning utilities."""
    
    def test_whitespace_cleaning(self):
        """Test removal of extra whitespace."""
        text = "  Hello    world   \n  test  "
        cleaned = clean_text(text)
        assert cleaned == "Hello world test"
    
    def test_control_character_removal(self):
        """Test removal of control characters."""
        text = "Hello\x00world\x01test"
        cleaned = clean_text(text)
        assert "\x00" not in cleaned
        assert "\x01" not in cleaned
        assert "Helloworldtest" in cleaned
    
    def test_whitespace_normalization(self):
        """Test normalization of whitespace including newlines and tabs."""
        text = "Line 1\nLine 2\tTabbed"
        cleaned = clean_text(text)
        assert cleaned == "Line 1 Line 2 Tabbed"
        assert "\n" not in cleaned
        assert "\t" not in cleaned
    
    def test_empty_input(self):
        """Test handling of empty input."""
        assert clean_text("") == ""
        assert clean_text(None) == ""
