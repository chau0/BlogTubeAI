"""
Unit tests for Transcript Handler (F02, F03)
"""

import pytest
from unittest.mock import patch, Mock
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from backend.src.core.transcript_handler import list_transcript_languages, fetch_transcript, clean_transcript_text


class TestListTranscriptLanguages:
    """Test F02: Language Selector functionality."""
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_successful_language_list(self, mock_get_instance):
        """Test successful transcript language listing."""
        mock_api = Mock()
        
        mock_transcript = Mock()
        mock_transcript.language_code = 'en'
        mock_transcript.language = 'English'
        mock_transcript.is_generated = False
        mock_transcript.is_translatable = True
        
        mock_api.list.return_value = [mock_transcript]
        mock_get_instance.return_value = mock_api
        
        languages = list_transcript_languages("dQw4w9WgXcQ")
        
        assert len(languages) == 1
        assert languages[0]['language_code'] == 'en'
        assert languages[0]['language'] == 'English'
        assert languages[0]['is_generated'] is False
        assert languages[0]['is_translatable'] is True
        
        # Verify the API was called correctly
        mock_api.list.assert_called_once_with("dQw4w9WgXcQ")
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_transcripts_disabled(self, mock_get_instance):
        """Test handling when transcripts are disabled."""
        mock_api = Mock()
        mock_api.list.side_effect = TranscriptsDisabled("video_id")
        mock_get_instance.return_value = mock_api
        
        with pytest.raises(Exception, match="Transcripts are disabled"):
            list_transcript_languages("dQw4w9WgXcQ")
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_video_unavailable(self, mock_get_instance):
        """Test handling when video is unavailable."""
        mock_api = Mock()
        mock_api.list.side_effect = VideoUnavailable("video_id")
        mock_get_instance.return_value = mock_api
        
        with pytest.raises(Exception, match="Video is unavailable"):
            list_transcript_languages("dQw4w9WgXcQ")


class TestFetchTranscript:
    """Test F03: Transcript Fetcher functionality."""
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_successful_transcript_fetch(self, mock_get_instance):
        """Test successful transcript fetching."""
        # Create a mock API instance
        mock_api = Mock()
        
        # Create mock FetchedTranscriptSnippet objects
        mock_snippet1 = Mock()
        mock_snippet1.text = "Hello world"
        mock_snippet1.start = 0.0
        mock_snippet1.duration = 2.0
        
        mock_snippet2 = Mock()
        mock_snippet2.text = "This is a test"
        mock_snippet2.start = 2.0
        mock_snippet2.duration = 3.0
        
        # Mock the fetch method to return an iterable of snippets
        mock_api.fetch.return_value = [mock_snippet1, mock_snippet2]
        mock_get_instance.return_value = mock_api
        
        transcript = fetch_transcript("dQw4w9WgXcQ", "en")
        assert "Hello world This is a test" in transcript
        
        # Verify the API was called correctly
        mock_api.fetch.assert_called_once_with("dQw4w9WgXcQ", languages=["en"])
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_translation_fallback(self, mock_get_instance):
        """Test fallback to translation when preferred language unavailable."""
        mock_api = Mock()
        
        # First call to fetch fails with NoTranscriptFound
        mock_api.fetch.side_effect = NoTranscriptFound("video_id", ["es"], [])
        
        # Setup mock transcript for the fallback list call
        mock_transcript = Mock()
        mock_transcript.is_translatable = True
        
        # Setup mock translated transcript
        mock_translated = Mock()
        mock_snippet = Mock()
        mock_snippet.text = "Translated text"
        mock_snippet.start = 0.0
        mock_snippet.duration = 2.0
        mock_translated.fetch.return_value = [mock_snippet]
        mock_transcript.translate.return_value = mock_translated
        
        mock_api.list.return_value = [mock_transcript]
        mock_get_instance.return_value = mock_api
        
        transcript = fetch_transcript("dQw4w9WgXcQ", "es")
        assert "Translated text" in transcript
        
        # Verify the API calls
        mock_api.fetch.assert_called_once_with("dQw4w9WgXcQ", languages=["es"])
        mock_api.list.assert_called_once_with("dQw4w9WgXcQ")
        mock_transcript.translate.assert_called_once_with("es")
    
    @patch('src.transcript_handler.get_youtube_api_instance')
    def test_no_transcript_available(self, mock_get_instance):
        """Test when no transcript is available."""
        mock_api = Mock()
        
        # First call to fetch fails
        mock_api.fetch.side_effect = NoTranscriptFound("video_id", ["en"], [])
        
        # Fallback call to list also fails
        mock_api.list.side_effect = Exception("No transcripts")
        mock_get_instance.return_value = mock_api
        
        transcript = fetch_transcript("dQw4w9WgXcQ", "en")
        assert transcript is None


class TestCleanTranscriptText:
    """Test transcript text cleaning functionality."""
    
    def test_basic_cleaning(self):
        """Test basic text cleaning."""
        dirty_text = "Hello   world  \n  This   is  a   test"
        clean_text = clean_transcript_text(dirty_text)
        assert clean_text == "Hello world This is a test"
    
    def test_remove_artifacts(self):
        """Test removal of transcript artifacts."""
        text_with_artifacts = "Hello [Music] world [Applause] test [Laughter]"
        clean_text = clean_transcript_text(text_with_artifacts)
        assert clean_text == "Hello world test"
    
    def test_fix_punctuation(self):
        """Test punctuation spacing fixes."""
        text_with_bad_punctuation = "Hello world . This is a test , right ?"
        clean_text = clean_transcript_text(text_with_bad_punctuation)
        assert clean_text == "Hello world. This is a test, right?"
    
    def test_empty_input(self):
        """Test handling of empty input."""
        assert clean_transcript_text("") == ""
        assert clean_transcript_text(None) == ""