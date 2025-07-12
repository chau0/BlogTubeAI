"""
Test configuration and fixtures
"""

import pytest
import tempfile
import os
from unittest.mock import Mock


@pytest.fixture
def sample_video_id():
    """Sample YouTube video ID for testing."""
    return "dQw4w9WgXcQ"


@pytest.fixture
def sample_url():
    """Sample YouTube URL for testing."""
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture
def sample_transcript():
    """Sample transcript content for testing."""
    return [
        {'text': 'Hello everyone', 'start': 0.0, 'duration': 2.0},
        {'text': 'Welcome to my video', 'start': 2.0, 'duration': 3.0},
        {'text': 'Today we will discuss', 'start': 5.0, 'duration': 4.0}
    ]


@pytest.fixture
def sample_blog_content():
    """Sample blog content for testing."""
    return """# Test Blog Post

## Introduction

This is a test blog post generated from a YouTube video.

## Main Content

The video discusses several important topics:

- Topic 1
- Topic 2
- Topic 3

## Conclusion

This concludes our discussion.
"""


@pytest.fixture
def temp_file():
    """Temporary file for testing file operations."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Generated blog content from OpenAI"
    return mock_response


@pytest.fixture
def mock_transcript_languages():
    """Mock transcript languages list."""
    return [
        {
            'language_code': 'en',
            'language': 'English',
            'is_generated': False,
            'is_translatable': True
        },
        {
            'language_code': 'es',
            'language': 'Spanish',
            'is_generated': True,
            'is_translatable': False
        }
    ]
