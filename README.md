# 🎬 BlogTubeAI - YouTube to Blog Converter

> Transform YouTube videos into engaging, AI-powered blog posts with intelligent content generation and multi-language support.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <img src="https://i.imgur.com/Ut5f5Qp.gif" alt="BlogTubeAI Demo" width="700"/>
</p>

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

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Make (for simplified workflow)
- At least one AI provider API key
- Internet connection for YouTube access

### 1. Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/BlogTubeAI.git
cd BlogTubeAI

# One-command setup (installs dependencies, creates directories, and .env template)
make setup
```

### 2. Configuration

After running `make setup`, configure your API keys:

```bash
# Edit the generated .env file with your API keys
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

### 3. Verify Setup

```bash
# Check that everything is configured correctly
make check-env

# Run a quick health check
make doctor
```

### 4. Basic Usage

```bash
# Start interactive mode for guided experience
make run

# Quick demo with a sample video
make demo

# Run with an example TED Talk
make example
```

## 📖 Usage

### Make Commands Overview

BlogTubeAI includes a comprehensive Makefile for streamlined development and usage:

```bash
# Get help with all available commands
make help

# Setup & Installation
make setup           # Complete development setup
make install         # Install production dependencies only
make dev-install     # Install development dependencies

# Application Usage
make run             # Start interactive mode
make demo            # Quick demo with sample video
make example         # Run with example TED Talk

# Development
make test            # Run all tests
make format          # Format code with black
make lint            # Run linter
make check-all       # Run all code quality checks

# Maintenance
make clean           # Remove cache files
make logs            # View recent logs
make version         # Show version info
```

### Command Line Options

For direct Python usage:
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
# Interactive mode - recommended for beginners
make run

# Direct command line usage
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
make run

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
│ Provider    │ Description         |
├─────────────┼─────────────────────┤
│ openai      │ OpenAI GPT models   |
│ claude      │ Anthropic Claude    |
│ gemini      │ Google Gemini       |
│ azureopenai │ Azure OpenAI        |
└─────────────┴─────────────────────┘

Select LLM provider [openai]: claude
```

## 📁 Project Structure

```
BlogTubeAI/
├── 📄 main.py                    # Main application entry point
├── 📄 Makefile                   # Development workflow automation
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
│   ├── 🧪 test_main.py
│   └── ⚙️ conftest.py
├── 📁 output/                    # Generated blog posts
├── 📁 logs/                      # Application logs
├── 📄 requirements.in            # Core dependencies
├── 📄 requirements-dev.in        # Development dependencies
├── 📄 .env.example              # Environment template
└── 📖 README.md                 # This file
```

## 🧪 Development

### Development Workflow

```bash
# Complete development setup
make dev

# Run tests before making changes
make test

# Format and lint your code
make format
make lint

# Run all quality checks
make check-all

# Pre-commit checks
make precommit
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-coverage

# Generate HTML coverage report
make test-html

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only

# Run tests in watch mode (requires pytest-watch)
make test-watch
```

### Dependency Management

```bash
# Add a new production dependency
make add-dep PACKAGE=package-name

# Add a new development dependency  
make add-dev-dep PACKAGE=package-name

# Upgrade all dependencies
make upgrade-deps

# Sync environment with requirements
make sync
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

### Quick Diagnostics

```bash
# Check environment and configuration
make check-env

# Run comprehensive health check
make doctor

# View recent application logs
make logs

# Check version and system info
make version
```

### Common Issues & Solutions

**❌ "No transcripts available"**
```bash
# Some videos don't have transcripts - check video settings
# Try a different video or check if captions are enabled
make demo  # Test with a known working video
```

**❌ "Invalid API key"** 
```bash
# Verify your .env file configuration
make check-env

# Test API key validity
python -c "import openai; print('OpenAI key valid')"
```

**❌ "Permission denied writing file"**
```bash
# Ensure output directory exists and has proper permissions
make create-dirs

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
make example  # Test with a known working example
```

### Development Issues

```bash
# Clean and reset environment
make clean-all
make dev-install

# Check code quality issues
make check-all

# Reset to fresh state
make reset
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

## 🤝 Contributing

We welcome contributions! Here's how to get started:

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/BlogTubeAI.git
cd BlogTubeAI

# Setup development environment
make dev

# Make your changes and test
make precommit

# Submit a pull request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

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

