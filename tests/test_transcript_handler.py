"""
Unit tests for Transcript Handler (F02, F03)
"""

import pytest
from unittest.mock import patch, Mock
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from src.transcript_handler import list_transcript_languages, fetch_transcript, clean_transcript_text


class TestListTranscriptLanguages:
    """Test F02: Language Selector functionality."""
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.list_transcripts')
    def test_successful_language_list(self, mock_list):
        """Test successful transcript language listing."""
        mock_transcript = Mock()
        mock_transcript.language_code = 'en'
        mock_transcript.language = 'English'
        mock_transcript.is_generated = False
        mock_transcript.is_translatable = True
        
        mock_list.return_value = [mock_transcript]
        
        languages = list_transcript_languages("dQw4w9WgXcQ")
        
        assert len(languages) == 1
        assert languages[0]['language_code'] == 'en'
        assert languages[0]['language'] == 'English'
        assert languages[0]['is_generated'] is False
        assert languages[0]['is_translatable'] is True
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.list_transcripts')
    def test_transcripts_disabled(self, mock_list):
        """Test handling when transcripts are disabled."""
        mock_list.side_effect = TranscriptsDisabled("video_id")
        
        with pytest.raises(Exception, match="Transcripts are disabled"):
            list_transcript_languages("dQw4w9WgXcQ")
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.list_transcripts')
    def test_video_unavailable(self, mock_list):
        """Test handling when video is unavailable."""
        mock_list.side_effect = VideoUnavailable("video_id")
        
        with pytest.raises(Exception, match="Video is unavailable"):
            list_transcript_languages("dQw4w9WgXcQ")


class TestFetchTranscript:
    """Test F03: Transcript Fetcher functionality."""
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.get_transcript')
    def test_successful_transcript_fetch(self, mock_get):
        """Test successful transcript fetching."""
        mock_get.return_value = [
            {'text': 'Hello world', 'start': 0.0, 'duration': 2.0},
            {'text': 'This is a test', 'start': 2.0, 'duration': 3.0}
        ]
        
        transcript = fetch_transcript("dQw4w9WgXcQ", "en")
        assert "Hello world This is a test" in transcript
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.get_transcript')
    @patch('src.transcript_handler.YouTubeTranscriptApi.list_transcripts')
    def test_translation_fallback(self, mock_list, mock_get):
        """Test fallback to translation when preferred language unavailable."""
        mock_get.side_effect = NoTranscriptFound("video_id", ["en"], [])
        
        mock_transcript = Mock()
        mock_transcript.is_translatable = True
        mock_translated = Mock()
        mock_translated.fetch.return_value = [
            {'text': 'Translated text', 'start': 0.0, 'duration': 2.0}
        ]
        mock_transcript.translate.return_value = mock_translated
        
        mock_list.return_value = [mock_transcript]
        
        transcript = fetch_transcript("dQw4w9WgXcQ", "es")
        assert "Translated text" in transcript
    
    @patch('src.transcript_handler.YouTubeTranscriptApi.get_transcript')
    @patch('src.transcript_handler.YouTubeTranscriptApi.list_transcripts')
    def test_no_transcript_available(self, mock_list, mock_get):
        """Test when no transcript is available."""
        mock_get.side_effect = NoTranscriptFound("video_id", ["en"], [])
        mock_list.side_effect = Exception("No transcripts")
        
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
