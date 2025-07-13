"""
Unit tests for Main CLI (F07, F09)
"""

import pytest
from unittest.mock import patch, Mock
from click.testing import CliRunner
from main import main


class TestMainCLI:
    """Test F07: CLI Interaction functionality."""
    
    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()
    
    @patch('main.get_video_id')
    @patch('main.validate_url')
    def test_invalid_url_handling(self, mock_validate, mock_get_id):
        """Test handling of invalid URLs."""
        mock_validate.return_value = False
        
        result = self.runner.invoke(main, ['https://invalid-url.com'])
        
        assert result.exit_code == 1
        assert "Invalid YouTube URL" in result.output
    
    @patch('main.get_video_id')
    @patch('main.validate_url')
    def test_no_video_id_extracted(self, mock_validate, mock_get_id):
        """Test handling when video ID cannot be extracted."""
        mock_validate.return_value = True
        mock_get_id.return_value = None
        
        result = self.runner.invoke(main, ['https://youtube.com/watch?v=invalid'])
        
        assert result.exit_code == 1
        assert "Could not extract video ID" in result.output
    
    @patch('main.list_transcript_languages')
    @patch('main.get_video_title')
    @patch('main.get_video_id')
    @patch('main.validate_url')
    def test_no_transcripts_available(self, mock_validate, mock_get_id, mock_get_title, mock_list_languages):
        """Test handling when no transcripts are available."""
        mock_validate.return_value = True
        mock_get_id.return_value = "dQw4w9WgXcQ"
        mock_get_title.return_value = "Test Video"
        mock_list_languages.return_value = []
        
        result = self.runner.invoke(main, ['https://youtube.com/watch?v=dQw4w9WgXcQ'])
        
        assert result.exit_code == 1
        assert "No transcripts available" in result.output
    
    @patch('main.save_blog_to_file')
    @patch('main.format_as_blog')
    @patch('main.LLMProviderFactory.create_provider')
    @patch('main.fetch_transcript')
    @patch('main.list_transcript_languages')
    @patch('main.get_video_title')
    @patch('main.get_video_id')
    @patch('main.validate_url')
    def test_successful_conversion(self, mock_validate, mock_get_id, mock_get_title, 
                                 mock_list_languages, mock_fetch, mock_create_provider,
                                 mock_format, mock_save):
        """Test successful video to blog conversion."""
        # Setup mocks
        mock_validate.return_value = True
        mock_get_id.return_value = "dQw4w9WgXcQ"
        mock_get_title.return_value = "Test Video"
        mock_list_languages.return_value = [{'language_code': 'en', 'language': 'English'}]
        mock_fetch.return_value = "This is a test transcript"
        
        mock_provider = Mock()
        mock_provider.generate_blog.return_value = "Generated blog content"
        mock_create_provider.return_value = mock_provider
        
        mock_format.return_value = "Formatted blog content"
        mock_save.return_value = True
        
        # Mock the Confirm.ask to avoid interactive prompts
        with patch('main.Confirm.ask', return_value=False):
            # Invoke the CLI command
            result = self.runner.invoke(main, [
                'https://youtube.com/watch?v=dQw4w9WgXcQ',
                '--language', 'en',
            ])
        
        # Assertions to validate the behavior
        assert result.exit_code == 0
        assert "Blog saved successfully" in result.output
        mock_validate.assert_called_once()
        mock_get_id.assert_called_once()
        mock_get_title.assert_called_once()
        mock_list_languages.assert_called_once()
        mock_fetch.assert_called_once()
        mock_create_provider.assert_called_once()
        mock_format.assert_called_once()
        mock_save.assert_called_once()
    
    def test_keyboard_interrupt_handling(self):
        """Test graceful handling of keyboard interrupt."""
        with patch('main.validate_url', side_effect=KeyboardInterrupt()):
            result = self.runner.invoke(main, ['https://youtube.com/watch?v=test'])
            
            assert result.exit_code == 0
            assert "Goodbye!" in result.output
    
    @patch('main.validate_url')
    def test_unexpected_error_handling(self, mock_validate):
        """Test handling of unexpected errors."""
        mock_validate.side_effect = Exception("Unexpected error")
        
        result = self.runner.invoke(main, ['https://youtube.com/watch?v=test'])
        
        assert result.exit_code == 1
        assert "Unexpected error" in result.output
    
    def test_interactive_mode(self):
        """Test interactive mode functionality."""
        with patch('main.Prompt.ask', return_value='https://youtube.com/watch?v=test'):
            with patch('main.validate_url', return_value=False):
                result = self.runner.invoke(main, ['--interactive'])
                
                assert result.exit_code == 1
                assert "Invalid YouTube URL" in result.output


class TestIntegration:
    """Test F09: Integration and modular testing support."""
    
    def test_module_imports(self):
        """Test that all modules can be imported successfully."""
        from src import youtube_parser
        from src import transcript_handler
        from src import llm_providers
        from src import blog_formatter
        from src import utils
        
        # Test that key functions are available
        assert hasattr(youtube_parser, 'get_video_id')
        assert hasattr(transcript_handler, 'fetch_transcript')
        assert hasattr(llm_providers, 'LLMProviderFactory')
        assert hasattr(blog_formatter, 'format_as_blog')
        assert hasattr(utils, 'validate_url')
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('src.llm_providers.openai')
    def test_end_to_end_pipeline(self, mock_openai):
        """Test the complete pipeline with mocked external calls."""
        from src.youtube_parser import get_video_id
        from src.utils import validate_url
        from src.llm_providers import LLMProviderFactory
        
        # Test the pipeline components work together
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Test URL validation
        assert validate_url(url) is True
        
        # Test video ID extraction
        video_id = get_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
        
        # Test LLM provider creation
        mock_openai.OpenAI.return_value = Mock()
        provider = LLMProviderFactory.create_provider('openai')
        assert provider is not None
