# 🎬 BlogTubeAI - YouTube to Blog Converter

> Transform YouTube videos into engaging, AI-powered blog posts with intelligent content generation and multi-language support.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

BlogTubeAI is an intelligent tool that converts YouTube video content into well-structured blog posts using advanced AI language models. It automatically extracts video transcripts, processes them through your choice of AI providers, and generates engaging, publication-ready blog content.

### 🎯 Perfect For

- **Content Creators** - Repurpose video content into blog posts
- **Marketers** - Create written content from webinars and presentations  
- **Educators** - Transform lecture videos into study materials
- **Bloggers** - Generate content from interview videos
- **Researchers** - Convert conference talks into readable articles

## ✨ Key Features

- 🌍 **Multi-language Support** - Extract transcripts in 50+ languages
- 🤖 **Multiple AI Providers** - OpenAI GPT, Anthropic Claude, Google Gemini, Azure OpenAI
- 🎨 **Smart Formatting** - Professional Markdown output with proper structure
- 💬 **Interactive CLI** - User-friendly command-line interface with Rich UI
- 📁 **Organized Output** - Automatic file naming and directory management
- 🔍 **Comprehensive Logging** - Daily log files for debugging and monitoring
- ⚡ **Error Handling** - Robust error management for private/unavailable videos
- 🔄 **Batch Processing** - Process multiple videos efficiently

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Core** | Python 3.8+ | Main application framework |
| **Transcripts** | youtube-transcript-api | YouTube transcript extraction |
| **AI Models** | OpenAI, Anthropic, Google | Content generation |
| **CLI Interface** | Rich + Click | Enhanced user experience |
| **Environment** | python-dotenv | Configuration management |
| **HTTP** | requests + urllib3 | API communications |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- At least one AI provider API key
- Internet connection for YouTube access

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/BlogTubeAI.git
cd BlogTubeAI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create your environment configuration:

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys
nano .env
```

Required environment variables:
```env
# Choose at least one provider
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
GOOGLE_API_KEY=your-gemini-key-here
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### 3. Basic Usage

```bash
# Convert any YouTube video to a blog post
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Interactive mode for guided experience
python main.py --interactive
```

## 📖 Detailed Usage Guide

### Command Line Options

```bash
python main.py [URL] [OPTIONS]

Arguments:
  URL                     YouTube video URL (optional in interactive mode)

Options:
  -l, --language TEXT     Transcript language (en, es, fr, de, etc.)
  -p, --provider CHOICE   AI provider [openai|claude|gemini|azureopenai]
  -o, --output PATH       Custom output file path
  -i, --interactive       Enable interactive mode
  --help                  Show help message and exit
```

### Real-World Examples

**1. Educational Content Processing:**
```bash
# Convert a lecture to a study guide
python main.py "https://youtu.be/lecture-video-id" \
  --language en \
  --provider openai \
  --output "study-guides/physics-101-lecture-5.md"
```

**2. Multi-language Content:**
```bash
# Process Spanish educational content
python main.py "https://youtu.be/spanish-video" \
  --language es \
  --provider claude
```

**3. Conference Talk Processing:**
```bash
# Convert tech conference presentation
python main.py "https://youtu.be/tech-talk" \
  --provider gemini \
  --output "conference-notes/ai-trends-2024.md"
```

**4. Batch Processing Script:**
```bash
#!/bin/bash
# process_videos.sh - Batch convert multiple videos

videos=(
    "https://youtu.be/video1"
    "https://youtu.be/video2" 
    "https://youtu.be/video3"
)

for video in "${videos[@]}"; do
    echo "Processing: $video"
    python main.py "$video" --provider openai
    sleep 5  # Rate limiting
done
```

### Interactive Mode Features

The interactive mode provides:
- ✅ URL validation and video preview
- 🌐 Language selection from available options
- 🤖 AI provider comparison and selection
- 📁 Custom output path specification
- 👀 Blog preview before saving

```bash
# Start interactive session
python main.py -i

# Example interactive session:
🎬 YouTube to Blog Converter
Transform videos into engaging blog posts!

Enter YouTube URL: https://youtu.be/example
✅ Video ID extracted: example
📹 Video: Amazing Tutorial Video

Available Transcript Languages:
┌──────┬─────────┐
│ Code │ Language│
├──────┼─────────┤
│ en   │ English │
│ es   │ Spanish │
│ fr   │ French  │
└──────┴─────────┘

Select language code [en]: en

Available LLM Providers:
┌─────────────┬─────────────────────┐
│ Provider    │ Description         │
├─────────────┼─────────────────────┤
│ openai      │ OpenAI GPT models   │
│ claude      │ Anthropic Claude    │
│ gemini      │ Google Gemini       │
│ azureopenai │ Azure OpenAI        │
└─────────────┴─────────────────────┘

Select LLM provider [openai]: claude
```

## 📁 Project Structure

```
BlogTubeAI/
├── 📄 main.py                    # Main application entry point
├── 📁 src/                       # Core application modules
│   ├── 🔗 youtube_parser.py      # URL parsing and video ID extraction
│   ├── 📝 transcript_handler.py  # Transcript fetching and processing
│   ├── 🤖 llm_providers.py       # AI provider integrations
│   ├── 📰 blog_formatter.py      # Markdown formatting and output
│   └── 🛠️ utils.py               # Utility functions and helpers
├── 📁 tests/                     # Comprehensive test suite
│   ├── 🧪 test_youtube_parser.py
│   ├── 🧪 test_transcript_handler.py
│   ├── 🧪 test_llm_providers.py
│   ├── 🧪 test_blog_formatter.py
│   ├── 🧪 test_utils.py
│   ├── 🧪 test_integration.py
│   └── ⚙️ conftest.py
├── 📁 output/                    # Generated blog posts
├── 📁 logs/                      # Application logs
├── 📄 requirements.in            # Core dependencies
├── 📄 requirements-dev.in        # Development dependencies
├── 📄 .env.example              # Environment template
└── 📖 README.md                 # This file
```

## 🧪 Testing & Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test categories
pytest tests/test_youtube_parser.py  # Unit tests
pytest tests/test_integration.py    # Integration tests

# Run with verbose output
pytest -v tests/
```

### Development Workflow

```bash
# Install development tools
pip install -r requirements-dev.in

# Code formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Run complete check
pytest --cov=src tests/ && black --check src/ && flake8 src/
```

### Test Coverage Goals

- 🎯 **Overall Coverage:** ≥90%
- 🎯 **Core Functions:** 100%
- 🎯 **Error Handling:** ≥95%
- 🎯 **Edge Cases:** ≥85%

## 📊 Performance Metrics

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| URL Parsing | < 1ms | Instant validation |
| Transcript Fetch | 1-5 seconds | Depends on video length |
| AI Generation | 10-45 seconds | Varies by provider & content |
| File Save | < 100ms | Local disk operation |
| **Total Workflow** | **15-60 seconds** | End-to-end processing |

### Optimization Tips

- 🚀 Use `--language en` for fastest transcript fetching
- ⚡ Choose OpenAI for fastest AI generation
- 📦 Process shorter videos (< 30 min) for optimal performance
- 🔄 Enable batch processing for multiple videos

## 🎨 Output Examples

### Generated Blog Structure

```markdown
# Video Title Here

**Source:** [Original Video](https://youtube.com/watch?v=example)
**Generated:** 2024-01-15

## Introduction
Engaging opening paragraph that hooks the reader...

## Main Content
### Key Point 1
Detailed explanation with insights...

### Key Point 2  
Further elaboration on important topics...

## Key Takeaways
- 📌 Important insight #1
- 📌 Important insight #2
- 📌 Important insight #3

## Conclusion
Thoughtful wrap-up that reinforces main themes...

---
*This blog post was generated from a YouTube video using BlogTubeAI.*
```

### File Naming Convention

Generated files follow this pattern:
```
output/
├── amazing_tutorial_video_dQw4w9WgXcQ.md
├── python_tips_and_tricks_xB2kF7pNvQ8.md
└── ai_explained_simply_mK9hR3tYw7L.md
```

## 🔧 Troubleshooting

### Common Issues & Solutions

**❌ "No transcripts available"**
```bash
# Some videos don't have transcripts - check video settings
# Try a different video or check if captions are enabled
```

**❌ "Invalid API key"** 
```bash
# Verify your .env file has correct API keys
cat .env | grep API_KEY

# Test API key validity
python -c "import openai; print('OpenAI key valid')"
```

**❌ "Permission denied writing file"**
```bash
# Ensure output directory permissions
mkdir -p output && chmod 755 output

# Or specify different output location
python main.py "URL" --output ~/Documents/blog.md
```

**❌ "Rate limit exceeded"**
```bash
# Wait and retry, or switch AI providers
python main.py "URL" --provider claude  # Try different provider
```

**❌ "Video unavailable"**
```bash
# Check if video is public and accessible
# Some videos are region-locked or private
```

### Debug Mode

```bash
# Enable detailed logging
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py "URL" --interactive  # More verbose output

# Check logs for detailed error information
tail -f logs/youtube-blog-converter_$(date +%Y-%m-%d).log
```

### Performance Issues

```bash
# Profile memory usage
pip install memory-profiler
python -m memory_profiler main.py "URL"

# Time operations
time python main.py "URL"
```

## 🌟 Advanced Features

### Custom AI Prompts

Modify `src/llm_providers.py` to customize blog generation:

```python
# Example: Add custom prompt for technical content
TECH_BLOG_PROMPT = """
Transform this transcript into a technical blog post with:
- Code examples where applicable
- Step-by-step tutorials
- Technical depth appropriate for developers
"""
```

### API Rate Limiting

Built-in rate limiting prevents API quota exhaustion:
- ⏰ OpenAI: 3 requests/minute (configurable)
- ⏰ Claude: 5 requests/minute
- ⏰ Gemini: 10 requests/minute

### Webhook Integration

Extend for automated processing:
```python
# Example webhook endpoint for automated blog generation
@app.route('/webhook/youtube', methods=['POST'])
def process_youtube_webhook():
    video_url = request.json.get('video_url')
    # Process with BlogTubeAI...
```

## 📈 Roadmap

### Upcoming Features

- 🎯 **v2.0** - Web interface with drag-and-drop
- 🔄 **v2.1** - Batch processing dashboard  
- 🌐 **v2.2** - Multiple output formats (PDF, HTML)
- 🎨 **v2.3** - Custom blog templates
- 📊 **v2.4** - Analytics and content insights
- 🔗 **v2.5** - CMS integration (WordPress, Ghost)

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Development setup
git clone https://github.com/yourusername/BlogTubeAI.git
cd BlogTubeAI
pip install -r requirements-dev.in
pytest  # Run tests before contributing
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 📧 **Email:** support@BlogTubeAI.com
- 💬 **Discord:** [BlogTubeAI Community](https://discord.gg/BlogTubeAI)
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/BlogTubeAI/issues)
- 📖 **Docs:** [Full Documentation](https://docs.BlogTubeAI.com)

## ⭐ Acknowledgments

- 🙏 **youtube-transcript-api** - For robust transcript extraction
- 🎨 **Rich** - For beautiful CLI interfaces
- 🤖 **OpenAI, Anthropic, Google** - For powerful AI models
- 👥 **Contributors** - For making this project better

---

<div align="center">

**Made with ❤️ by the BlogTubeAI Team**

[⭐ Star us on GitHub](https://github.com/yourusername/BlogTubeAI) | [🐦 Follow on Twitter](https://twitter.com/BlogTubeAI) | [📧 Newsletter](https://newsletter.BlogTubeAI.com)

</div>

