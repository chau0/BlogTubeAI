"""
Unit tests for LLM Providers (F04)
"""

import pytest
from unittest.mock import patch, Mock, MagicMock
from backend.src.core.llm_providers import LLMProvider, OpenAIProvider, AzureOpenAIProvider, ClaudeProvider, GeminiProvider, LLMProviderFactory


class TestLLMProvider:
    """Test abstract LLM provider functionality."""
    
    def test_create_blog_prompt(self):
        """Test blog prompt creation."""
        provider = OpenAIProvider.__new__(OpenAIProvider)  # Create without __init__
        
        prompt = provider.create_blog_prompt(
            "This is a test transcript", 
            "Test Video", 
            "https://youtube.com/watch?v=test"
        )
        
        assert "Test Video" in prompt
        assert "This is a test transcript" in prompt
        assert "https://youtube.com/watch?v=test" in prompt
        assert "Markdown" in prompt


class TestOpenAIProvider:
    """Test OpenAI provider functionality."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('src.llm_providers.openai')
    def test_initialization(self, mock_openai):
        """Test OpenAI provider initialization."""
        mock_openai.OpenAI.return_value = Mock()
        provider = OpenAIProvider()
        assert provider.client is not None
    
    def test_missing_api_key(self):
        """Test error when API key is missing."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                OpenAIProvider()
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('src.llm_providers.openai')
    def test_generate_blog_success(self, mock_openai):
        """Test successful blog generation."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated blog content"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        
        provider = OpenAIProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result == "Generated blog content"
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('src.llm_providers.openai')
    def test_generate_blog_failure(self, mock_openai):
        """Test blog generation failure handling."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.OpenAI.return_value = mock_client
        
        provider = OpenAIProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result is None


class TestAzureOpenAIProvider:
    """Test Azure OpenAI provider functionality."""
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4-deployment'
    })
    @patch('src.llm_providers.openai')
    def test_initialization(self, mock_openai):
        """Test Azure OpenAI provider initialization."""
        mock_openai.AzureOpenAI.return_value = Mock()
        provider = AzureOpenAIProvider()
        assert provider.client is not None
        assert provider.deployment_name == 'gpt-4-deployment'
    
    def test_missing_api_key(self):
        """Test error when API key is missing."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="AZURE_OPENAI_API_KEY"):
                AzureOpenAIProvider()
    
    def test_missing_endpoint(self):
        """Test error when endpoint is missing."""
        with patch.dict('os.environ', {'AZURE_OPENAI_API_KEY': 'test-key'}, clear=True):
            with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
                AzureOpenAIProvider()
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/'
    })
    @patch('src.llm_providers.openai')
    def test_default_deployment_name(self, mock_openai):
        """Test default deployment name when not specified."""
        mock_openai.AzureOpenAI.return_value = Mock()
        provider = AzureOpenAIProvider()
        assert provider.deployment_name == 'gpt-4.1'
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'custom-deployment'
    })
    @patch('src.llm_providers.openai')
    def test_generate_blog_success(self, mock_openai):
        """Test successful blog generation with Azure OpenAI."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Azure OpenAI generated content"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.AzureOpenAI.return_value = mock_client
        
        provider = AzureOpenAIProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result == "Azure OpenAI generated content"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/'
    })
    @patch('src.llm_providers.openai')
    def test_generate_blog_failure(self, mock_openai):
        """Test blog generation failure handling."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("Azure API Error")
        mock_openai.AzureOpenAI.return_value = mock_client
        
        provider = AzureOpenAIProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result is None


class TestClaudeProvider:
    """Test Claude provider functionality."""
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('src.llm_providers.anthropic')
    def test_initialization(self, mock_anthropic):
        """Test Claude provider initialization."""
        mock_anthropic.Anthropic.return_value = Mock()
        provider = ClaudeProvider()
        assert provider.client is not None
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    @patch('src.llm_providers.anthropic')
    def test_generate_blog_success(self, mock_anthropic):
        """Test successful blog generation with Claude."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Claude generated content"
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client
        
        provider = ClaudeProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result == "Claude generated content"


class TestGeminiProvider:
    """Test Gemini provider functionality."""
    
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    @patch('src.llm_providers.genai')
    def test_initialization(self, mock_genai):
        """Test Gemini provider initialization."""
        mock_model = Mock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider()
        assert provider.model is not None
    
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
    @patch('src.llm_providers.genai')
    def test_generate_blog_success(self, mock_genai):
        """Test successful blog generation with Gemini."""
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Gemini generated content"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        provider = GeminiProvider()
        result = provider.generate_blog("transcript", "title", "url")
        
        assert result == "Gemini generated content"


class TestLLMProviderFactory:
    """Test LLM provider factory."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    @patch('src.llm_providers.openai')
    def test_create_openai_provider(self, mock_openai):
        """Test creating OpenAI provider."""
        mock_openai.OpenAI.return_value = Mock()
        provider = LLMProviderFactory.create_provider('openai')
        assert isinstance(provider, OpenAIProvider)
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/'
    })
    @patch('src.llm_providers.openai')
    def test_create_azureopenai_provider(self, mock_openai):
        """Test creating Azure OpenAI provider."""
        mock_openai.AzureOpenAI.return_value = Mock()
        provider = LLMProviderFactory.create_provider('azureopenai')
        assert isinstance(provider, AzureOpenAIProvider)
    
    def test_unsupported_provider(self):
        """Test error for unsupported provider."""
        with pytest.raises(ValueError, match="Unsupported provider"):
            LLMProviderFactory.create_provider('unsupported')
