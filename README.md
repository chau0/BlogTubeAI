# YouTube to Blog Converter

Transform YouTube videos into well-formatted blog posts using AI-powered transcription and content generation.

## 📋 Overview

This tool automates the process of converting YouTube video content into engaging blog posts by:

1. **Extracting video ID** from YouTube URL
2. **Fetching available transcript languages** 
3. **Allowing language selection** for transcripts
4. **Downloading video transcript** 
5. **Processing content with LLM** for blog generation
6. **Outputting formatted Markdown** blog post

## 🚀 Features

- Support for multiple transcript languages
- Interactive CLI interface
- Multiple LLM provider support (OpenAI, Claude, Gemini)
- Customizable blog formatting
- Markdown output with proper structure
- Error handling for private/unavailable videos

## 🛠️ Tech Stack

- **Python 3.8+** - Core language
- **youtube-transcript-api** - YouTube transcript extraction
- **openai** - OpenAI GPT integration
- **anthropic** - Claude AI integration (optional)
- **google-generativeai** - Gemini AI integration (optional)
- **rich** - Enhanced CLI interface and formatting
- **click** - Command-line interface framework
- **requests** - HTTP requests handling
- **python-dotenv** - Environment variable management

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd youtube-tool
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## ⚙️ Configuration

Create a `.env` file with your LLM API credentials:

```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_claude_key_here
GOOGLE_API_KEY=your_gemini_key_here
```

## 🎯 Usage

### Prerequisites
- Python 3.8 or higher
- At least one LLM API key (OpenAI, Anthropic, or Google)
- Internet connection for YouTube API access

### Basic Usage
```bash
# Convert a YouTube video to blog post
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Specify language and provider
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --language en --provider openai

# Save to specific file
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output my_blog_post.md
```

### Interactive Mode
```bash
# Start interactive session
python main.py --interactive

# Or simply run without URL
python main.py
```

### Command Line Options
```bash
python main.py [URL] [OPTIONS]

Options:
  -l, --language TEXT     Transcript language code (en, es, fr, etc.)
  -p, --provider TEXT     LLM provider: openai, claude, gemini [default: openai]
  -o, --output TEXT       Output file path
  -i, --interactive       Start interactive mode
  --help                  Show help message
```

### Example Workflows

**1. Quick Blog Generation:**
```bash
# One-line conversion with defaults
python main.py "https://youtu.be/dQw4w9WgXcQ"
```

**2. Spanish Content:**
```bash
# Extract Spanish transcript and generate blog
python main.py "https://youtu.be/dQw4w9WgXcQ" --language es --provider claude
```

**3. Batch Processing:**
```bash
# Process multiple videos (create a script)
#!/bin/bash
urls=(
    "https://youtu.be/video1"
    "https://youtu.be/video2"
    "https://youtu.be/video3"
)

for url in "${urls[@]}"; do
    python main.py "$url" --provider openai
done
```

**4. Custom Output Directory:**
```bash
# Save to specific directory
mkdir -p output/blogs
python main.py "https://youtu.be/dQw4w9WgXcQ" --output output/blogs/my_blog.md
```

### Expected Output
When successful, you'll see:
```
🎬 YouTube to Blog Converter
Transform videos into engaging blog posts!

✅ Video ID extracted: dQw4w9WgXcQ
📹 Video: Rick Astley - Never Gonna Give You Up (Official Video)
🔍 Fetching available transcript languages...

Available Transcript Languages
┌──────┬─────────┐
│ Code │ Language│
├──────┼─────────┤
│ en   │ English │
│ es   │ Spanish │
└──────┴─────────┘

📝 Fetching transcript in 'en'...
✅ Transcript fetched (2847 characters)
🤖 Generating blog using openai...
🎉 Blog saved successfully to: rick_astley_never_gonna_give_you_up_official_video_dQw4w9WgXcQ.md
```

## 🧪 Testing

### Test Structure
```
tests/
├── __init__.py
├── test_youtube_parser.py      # URL parsing and video ID extraction
├── test_transcript_handler.py  # Transcript fetching and processing
├── test_llm_providers.py       # LLM integration (mocked)
├── test_blog_formatter.py      # Markdown formatting and file I/O
├── test_utils.py               # Utility functions
├── test_integration.py         # End-to-end workflow tests
└── conftest.py                 # Test configuration and fixtures
```

### Setting Up Tests

**1. Install test dependencies:**
```bash
pip install pytest pytest-mock pytest-cov
```

**2. Set up test environment:**
```bash
# Create test environment file
cp .env.example .env.test
echo "OPENAI_API_KEY=test_key" >> .env.test
echo "ANTHROPIC_API_KEY=test_key" >> .env.test
echo "GOOGLE_API_KEY=test_key" >> .env.test
```

### Running Tests

**Basic Test Execution:**
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_youtube_parser.py

# Run specific test function
pytest tests/test_youtube_parser.py::TestGetVideoId::test_standard_youtube_url
```

**Coverage Testing:**
```bash
# Run tests with coverage report
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html  # View coverage report

# Coverage with missing lines
pytest --cov=src --cov-report=term-missing tests/
```

**Test Categories:**
```bash
# Run only unit tests
pytest tests/ -k "not integration"

# Run only integration tests
pytest tests/test_integration.py

# Run tests for specific module
pytest tests/test_youtube_parser.py tests/test_utils.py
```

**Performance and Load Testing:**
```bash
# Run tests with timing
pytest --durations=10

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Test Examples

**Manual Testing Scenarios:**

**1. Test with Real YouTube Video:**
```bash
# Use a known public video for testing
python main.py "https://www.youtube.com/watch?v=jNQXAC9IVRw" --provider openai
```

**2. Test Error Handling:**
```bash
# Test with invalid URL
python main.py "https://example.com/fake-video"

# Test with private video
python main.py "https://www.youtube.com/watch?v=invalid_video_id"

# Test with missing API key
unset OPENAI_API_KEY
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**3. Test Different Languages:**
```bash
# Test Spanish transcript
python main.py "https://www.youtube.com/watch?v=spanish_video_id" --language es

# Test automatic translation
python main.py "https://www.youtube.com/watch?v=english_video_id" --language fr
```

### Debugging Tests

**Run Tests in Debug Mode:**
```bash
# Drop into debugger on failure
pytest --pdb

# Run with print statements visible
pytest -s

# Run single test with debugging
pytest -s -vvv tests/test_youtube_parser.py::test_get_video_id
```

**Mock Testing:**
```bash
# Test with mocked APIs (no real API calls)
export PYTEST_MOCK_MODE=true
pytest tests/test_llm_providers.py
```

### Continuous Integration

**GitHub Actions Example (`.github/workflows/test.yml`):**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest --cov=src tests/
```

### Performance Benchmarks

**Expected Performance:**
- URL parsing: < 1ms
- Transcript fetching: 1-5 seconds
- LLM generation: 10-30 seconds
- File saving: < 100ms
- Total workflow: 15-45 seconds

**Benchmark Testing:**
```bash
# Time the full workflow
time python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Profile memory usage
python -m memory_profiler main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Troubleshooting

**Common Issues:**

**1. Import Errors:**
```bash
# Ensure src directory is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**2. API Key Issues:**
```bash
# Verify environment variables
python -c "import os; print('OpenAI:', bool(os.getenv('OPENAI_API_KEY')))"
```

**3. Network Issues:**
```bash
# Test with offline mode (mocked tests only)
pytest tests/ -k "not integration and not network"
```

**4. Permission Errors:**
```bash
# Ensure write permissions for output directory
mkdir -p output && chmod 755 output
python main.py "https://youtu.be/dQw4w9WgXcQ" --output output/test.md
```

### Test Data Management

**Fixtures and Test Data:**
```python
# tests/conftest.py contains shared test data
SAMPLE_VIDEO_ID = "dQw4w9WgXcQ"
SAMPLE_TRANSCRIPT = "Hello everyone, welcome to my channel..."
MOCK_BLOG_CONTENT = "# Amazing Blog Post\n\nThis is content..."
```

**Environment-Specific Testing:**
```bash
# Test with different Python versions
python3.8 -m pytest tests/
python3.9 -m pytest tests/
python3.10 -m pytest tests/
```

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v tests/
```

### 📊 Test Coverage Goals

- **Overall Coverage:** ≥90%
- **Core Functions:** 100%
- **Error Handling:** ≥95%
- **Edge Cases:** ≥85%

## 📝 Example Output

The tool generates structured blog posts with:
- Engaging title
- Introduction paragraph
- Main content sections
- Key takeaways
- Conclusion
- Proper Markdown formatting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Limitations

- Requires publicly available YouTube videos with transcripts
- API rate limits apply based on chosen LLM provider
- Transcript quality depends on YouTube's auto-generation

## 🔗 Related Projects

- [BlogForgeAI](../README.md) - Main project repository

