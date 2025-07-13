"""
Unit tests for Blog Formatter (F05, F06)
"""

import pytest
import tempfile
import os
from unittest.mock import patch, mock_open
from src.core.blog_formatter import format_as_blog, save_blog_to_file, create_blog_summary, validate_markdown


class TestFormatAsBlog:
    """Test F05: Markdown Formatter functionality."""
    
    def test_format_with_metadata(self):
        """Test blog formatting with metadata."""
        content = "# Test Blog\n\nThis is test content."
        title = "Test Video"
        url = "https://youtube.com/watch?v=test"
        
        formatted = format_as_blog(content, title, url)
        
        assert "---" in formatted  # YAML frontmatter
        assert "title:" in formatted
        assert "date:" in formatted
        assert "source:" in formatted
        assert url in formatted
        assert title in formatted
        assert content in formatted
    
    def test_attribution_included(self):
        """Test that attribution is included."""
        content = "Test content"
        title = "Test Video"
        url = "https://youtube.com/watch?v=test"
        
        formatted = format_as_blog(content, title, url)
        
        assert "This blog post was generated" in formatted
        assert "Generated on" in formatted


class TestSaveBlogToFile:
    """Test F06: File Writer functionality."""
    
    def test_save_to_file(self):
        """Test saving blog to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            temp_path = f.name
        
        try:
            content = "# Test Blog\n\nTest content"
            result = save_blog_to_file(content, temp_path)
            
            assert result is True
            assert os.path.exists(temp_path)
            
            with open(temp_path, 'r') as f:
                saved_content = f.read()
            assert saved_content == content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_add_md_extension(self):
        """Test automatic .md extension addition."""
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test_file")
            content = "Test content"
            
            result = save_blog_to_file(content, filename)
            
            assert result is True
            assert os.path.exists(filename + ".md")
    
    def test_create_directory(self):
        """Test directory creation if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_directory")
            filename = os.path.join(new_dir, "test.md")
            content = "Test content"
            
            result = save_blog_to_file(content, filename)
            
            assert result is True
            assert os.path.exists(filename)
    
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_save_failure(self, mock_file):
        """Test handling of save failures."""
        result = save_blog_to_file("content", "test.md")
        assert result is False


class TestCreateBlogSummary:
    """Test blog summary creation."""
    
    def test_extract_summary(self):
        """Test summary extraction from content."""
        content = """---
title: Test
---

# Blog Title

This is the first paragraph that should be used as summary. 
It contains multiple sentences to test the extraction.

## Section 2

More content here.
"""
        summary = create_blog_summary(content)
        assert "This is the first paragraph" in summary
        assert len(summary) <= 200
    
    def test_truncate_long_summary(self):
        """Test summary truncation for long content."""
        long_content = "A" * 300
        content = f"# Title\n\n{long_content}"
        
        summary = create_blog_summary(content)
        assert len(summary) <= 200
        assert summary.endswith("...")


class TestValidateMarkdown:
    """Test Markdown validation."""
    
    def test_valid_markdown(self):
        """Test validation of valid Markdown."""
        # read a sample Markdown content from a file
        with open('tests/test_core/data/long_text_500word.md', 'r', encoding='utf-8') as f:
            content = f.read()
        assert validate_markdown(content) is True
    
    def test_invalid_short_content(self):
        """Test rejection of too short content."""
        content = "# Title\n\nShort."
        assert validate_markdown(content) is False
    
    def test_invalid_no_headers(self):
        """Test rejection of content without headers."""
        content = "This is just plain text without any headers. " * 50
        assert validate_markdown(content) is False
    
    def test_empty_content(self):
        """Test rejection of empty content."""
        assert validate_markdown("") is False
        assert validate_markdown(None) is False
