"""
LLM Provider Integrations
Support for multiple AI providers to generate blog content.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_blog(self, transcript: str, title: str, url: str) -> Optional[str]:
        """Generate blog content from transcript."""
        pass
    
    def create_blog_prompt(self, transcript: str, title: str, url: str) -> str:
        """Create a standardized prompt for blog generation."""
        return f"""
Please convert the following YouTube video transcript into a well-structured, engaging blog post optimized for Medium publishing.

Video Title: {title}
Video URL: {url}

Requirements for Medium Blog Post:
1. Create a compelling, SEO-friendly title that would perform well on Medium
2. Write an engaging introduction that hooks Medium readers within the first 3 sentences
3. Structure content with clear sections using Medium-style headings (##, ###)
4. Extract key insights and actionable takeaways from the transcript
5. Use a conversational, storytelling tone that resonates with Medium's audience
6. Include personal insights or commentary to add unique value
7. Add a strong conclusion with clear call-to-action
8. Format in Markdown with proper Medium formatting
9. Aim for 1000-2000 words for optimal Medium engagement
10. Include strategic image placement suggestions

IMPORTANT - Image Integration:
At appropriate points throughout the blog post, insert image generation prompts using this format:
[IMAGE_PROMPT: Detailed description of image to generate for this section]

Insert image prompts for:
- Hero image after the title
- Concept illustrations for key points
- Visual metaphors for complex ideas
- Summary or conclusion visuals

Example image prompt format:
[IMAGE_PROMPT: A modern, minimalist illustration showing a person at a desk with multiple screens displaying data analytics dashboards, soft lighting, professional atmosphere, digital art style]

Transcript:
{transcript}

Generate a Medium-ready blog post with strategic image placement prompts:
"""

class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self):
        if not openai:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_blog(self, transcript: str, title: str, url: str) -> Optional[str]:
        """Generate blog using OpenAI GPT."""
        try:
            prompt = self.create_blog_prompt(transcript, title, url)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates engaging blog posts from video transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return None

class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI provider."""
    
    def __init__(self):
        if not openai:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
        
        if not api_key:
            raise ValueError("AZURE_OPENAI_API_KEY environment variable not set")
        if not endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable not set")
        
        self.client = openai.AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )
        
        # Use deployment name from environment, default to gpt-4
        self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4')
    
    def generate_blog(self, transcript: str, title: str, url: str) -> Optional[str]:
        """Generate blog using Azure OpenAI."""
        try:
            prompt = self.create_blog_prompt(transcript, title, url)
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates engaging blog posts from video transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Azure OpenAI API error: {str(e)}")
            return None

class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self):
        if not anthropic:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_blog(self, transcript: str, title: str, url: str) -> Optional[str]:
        """Generate blog using Claude."""
        try:
            prompt = self.create_blog_prompt(transcript, title, url)
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API error: {str(e)}")
            return None

class GeminiProvider(LLMProvider):
    """Google Gemini provider."""
    
    def __init__(self):
        if not genai:
            raise ImportError("Google AI package not installed. Run: pip install google-generativeai")
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_blog(self, transcript: str, title: str, url: str) -> Optional[str]:
        """Generate blog using Gemini."""
        try:
            prompt = self.create_blog_prompt(transcript, title, url)
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Gemini API error: {str(e)}")
            return None

class LLMProviderFactory:
    """Factory class to create LLM providers."""
    
    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        """Create an LLM provider instance."""
        provider_name = provider_name.lower()
        
        if provider_name == 'openai':
            return OpenAIProvider()
        elif provider_name == 'azureopenai':
            return AzureOpenAIProvider()
        elif provider_name == 'claude':
            return ClaudeProvider()
        elif provider_name == 'gemini':
            return GeminiProvider()
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
