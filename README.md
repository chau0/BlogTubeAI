# 🎬 BlogTubeAI - YouTube to Blog Converter

> Transform YouTube videos into engaging, AI-powered blog posts with intelligent content generation and multi-language support.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <img src="https://i.imgur.com/Ut5f5Qp.gif" alt="BlogTubeAI Demo" width="700"/>
</p>

## 📋 Overview

BlogTubeAI is an intelligent tool that converts YouTube video content into well-structured blog posts using advanced AI language models. It features both a powerful **CLI application** and a modern **web interface** with real-time progress tracking.

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
- 💻 **CLI + Web Interface** - Choose between command-line or browser-based UI
- 📊 **Real-time Progress** - WebSocket-powered live updates (web interface)
- 📁 **Organized Output** - Automatic file naming and directory management
- 🔍 **Comprehensive Logging** - Daily log files for debugging and monitoring
- ⚡ **Error Handling** - Robust error management for private/unavailable videos
- 🏗️ **Modular Architecture** - Clean separation between CLI and web components

## 🏗️ Project Architecture

```
BlogTubeAI/
├── 📄 main.py                          # CLI Application Entry Point
├── 📁 backend/                         # Backend & Core Logic
│   ├── 📁 src/
│   │   ├── 📁 core/                    # Core Business Logic (migrated from Phase 1)
│   │   │   ├── 🔗 youtube_parser.py    # YouTube URL parsing & video info
│   │   │   ├── 📝 transcript_handler.py # Transcript fetching & processing
│   │   │   ├── 🤖 llm_providers.py     # AI provider integrations
│   │   │   ├── 📰 blog_formatter.py    # Markdown formatting & output
│   │   │   └── 🛠️ utils.py             # Utility functions
│   │   ├── 📁 web/                     # FastAPI Web Application
│   │   ├── 📁 api/                     # REST API Endpoints
│   │   ├── 📁 models/                  # Data Models & Schemas
│   │   └── 📁 services/                # Business Logic Services
│   ├── 📁 tests/                       # Comprehensive Test Suite
│   │   ├── 📁 test_core/               # Core Module Tests
│   │   ├── 📁 test_web/                # Web API Tests
│   │   └── 🧪 test_main.py             # CLI Integration Tests
│   └── 📄 Makefile                     # Backend Development Commands
├── 📁 frontend/                        # React Web Interface
│   ├── 📁 src/
│   │   ├── 📁 components/              # React Components
│   │   ├── 📁 pages/                   # Page Components
│   │   ├── 📁 hooks/                   # Custom React Hooks
│   │   └── 📁 lib/                     # Utilities & API Client
│   └── 📄 package.json                 # Frontend Dependencies
├── 📁 docs/                            # Documentation
└── 📄 Makefile                         # Project Orchestrator
```

## 🛠️ Tech Stack

### **Core Architecture**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Core Logic** | Python 3.8+ | Shared business logic |
| **CLI Interface** | Rich + Click | Command-line experience |
| **Web Backend** | FastAPI | REST API + WebSockets |
| **Web Frontend** | React 18 + TypeScript + Vite | Modern web interface |
| **Database** | SQLite/PostgreSQL | Job tracking & history |

### **AI & External APIs**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Transcripts** | youtube-transcript-api | YouTube transcript extraction |
| **AI Models** | OpenAI, Anthropic, Google | Content generation |
| **Environment** | python-dotenv | Configuration management |

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** for CLI and backend
- **Node.js 16+** for web interface (optional)
- At least one AI provider API key
- Internet connection for YouTube access

### 1. Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/BlogTubeAI.git
cd BlogTubeAI

# Complete project setup (CLI + Backend + Frontend)
make setup
```

### 2. Configuration

Configure your API keys in the backend:

```bash
# Edit the backend environment file
nano backend/.env
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

### 3. Choose Your Interface

#### Option A: CLI Application (Fastest Start)
```bash
# Start CLI in interactive mode
make cli-run

# Or run directly
python main.py --interactive
```

#### Option B: Web Interface (Full Experience)
```bash
# Start both backend and frontend
make dev

# This starts:
# - Backend API on http://localhost:8000
# - Frontend app on http://localhost:5173
```

#### Option C: Backend Only (API Development)
```bash
# Start just the backend API
make backend-dev
```

## 📖 Usage Guide

### CLI Application

The CLI provides the fastest way to convert videos:

```bash
# Interactive mode (recommended)
make cli-run

# Direct URL processing
python main.py "https://youtu.be/video-id" --provider openai

# Batch processing with custom options
python main.py "https://youtu.be/video-id" \
  --language es \
  --provider claude \
  --output "articles/my-blog-post.md"
```

**CLI Features:**
- ✅ Interactive video URL input with validation
- ✅ Language selection from available transcripts
- ✅ AI provider comparison and selection
- ✅ Real-time progress display
- ✅ Instant blog preview and save

### Web Interface

The web interface provides a modern, user-friendly experience:

```bash
# Start web interface
make dev
# Visit http://localhost:5173
```

**Web Features:**
- 🎨 **Beautiful UI** - Modern React interface with dark/light themes
- 📊 **Real-time Progress** - Live updates via WebSocket
- 📝 **Multi-step Workflow** - Guided conversion process
- 📚 **Job History** - Track and manage previous conversions
- 💾 **Download Options** - Multiple export formats
- 📱 **Mobile Responsive** - Works on all devices

### Development Commands

The project includes comprehensive Makefiles for development:

#### **Project-Level Commands (Root Makefile)**
```bash
make help              # Show all available commands
make setup             # Complete project setup
make dev               # Start full development environment
make test-all          # Run all tests (CLI + Backend + Frontend)
make clean             # Clean all components
make check-env         # Check project environment

# Component-specific commands
make cli               # CLI application commands
make backend           # Backend development commands  
make frontend          # Frontend development commands
```

#### **CLI Application Commands**
```bash
make cli-run           # Run CLI interactively
make cli-demo          # Run CLI demo
make cli-test          # Test CLI functionality
```

#### **Backend Development Commands**
```bash
make -C backend help          # Show backend commands
make -C backend setup         # Setup backend environment
make -C backend run-dev       # Start FastAPI development server
make -C backend test          # Run backend tests
make -C backend test-core     # Test core modules
make -C backend test-web      # Test web APIs
```

#### **Frontend Development Commands**
```bash
make -C frontend help         # Show frontend commands
make -C frontend install      # Install dependencies
make -C frontend dev          # Start development server
make -C frontend build        # Build for production
make -C frontend test         # Run frontend tests
```

## 📁 Updated Project Structure

### **After Migration Benefits:**

1. **Unified Core Logic** - All business logic in `backend/src/core/`
2. **Clean Separation** - CLI, Backend API, and Frontend clearly separated
3. **Shared Testing** - Core module tests in `backend/tests/test_core/`
4. **Scalable Architecture** - Ready for both Phase 1 (CLI) and Phase 2 (Web) 
5. **Professional Organization** - Follows Python/React project best practices

### **Import Structure:**
```python
# CLI Application (main.py)
from backend.src.core.youtube_parser import get_video_id, get_video_title
from backend.src.core.llm_providers import LLMProviderFactory

# Backend Web APIs
from ..core.youtube_parser import get_video_id  # Clean relative imports
from ..core.llm_providers import LLMProviderFactory

# Tests
from backend.src.core.youtube_parser import get_video_id  # Absolute imports
```

## 🧪 Testing & Quality

### **Comprehensive Test Coverage**
```bash
# Run all tests across the project
make test-all

# Component-specific testing
make cli-test                    # CLI functionality
make -C backend test-core        # Core business logic
make -C backend test-web         # Web APIs
make -C frontend test            # Frontend components
```

### **Code Quality Tools**
```bash
# Format and lint (backend)
make -C backend format
make -C backend lint

# Type checking
make -C backend type-check

# Pre-commit checks
make precommit
```

## 🌟 Advanced Features

### **Real-time Web Interface**
- WebSocket-powered live progress updates
- Multi-step conversion workflow with validation
- Job history with search and filtering
- Download management with multiple formats

### **Robust CLI Application**
- Interactive mode with Rich UI components
- Batch processing capabilities
- Comprehensive error handling
- Daily rotating log files

### **Developer Experience**
- Hot reload for both frontend and backend development
- Comprehensive testing with mocking
- API documentation auto-generation
- Docker support for deployment

## 📊 Performance Metrics

| Operation | CLI Time | Web Time | Notes |
|-----------|----------|----------|-------|
| URL Parsing | < 1ms | < 1ms | Instant validation |
| Transcript Fetch | 1-5s | 1-5s | Depends on video length |
| AI Generation | 10-45s | 10-45s | Real-time progress in web |
| File Save | < 100ms | < 100ms | Local/server storage |
| **Total Workflow** | **15-60s** | **15-60s** | **Both interfaces** |

## 🔧 Deployment

### **CLI Deployment**
```bash
# Package for distribution
make build-cli

# Install as system command
pip install -e .
```

### **Web Deployment**
```bash
# Build frontend for production
make -C frontend build

# Start production server
make -C backend run-prod

# Docker deployment
make docker-build
make docker-run
```

## 🛠️ Troubleshooting

### **Quick Diagnostics**
```bash
# Check entire project environment
make check-env

# Component-specific checks
make -C backend check-env
make -C frontend check
```

### **Common Issues**

**❌ "Module not found" after migration**
```bash
# Ensure you're running from project root
cd BlogTubeAI
python main.py --help

# Or use make commands
make cli-run
```

**❌ "Backend API not accessible"**
```bash
# Check if backend is running
make -C backend run-dev

# Verify frontend proxy configuration
cat frontend/vite.config.ts
```

**❌ "Tests failing after migration"**
```bash
# Run tests from correct locations
make -C backend test-core      # Core module tests
make test-all                  # All project tests
```

## 📈 Roadmap

### **Current Status**
- ✅ **Phase 1**: Full-featured CLI application (99% complete)
- ✅ **Migration**: Unified project structure (100% complete)
- 🚧 **Phase 2**: Web interface backend (in development)
- 📋 **Phase 2**: Frontend integration (ready for backend)

### **Upcoming Features**
- 🔄 **v2.0** - Complete web interface with real-time progress
- 📊 **v2.1** - Advanced analytics and content insights
- 🌐 **v2.2** - Multiple output formats (PDF, HTML, DOCX)
- 🎨 **v2.3** - Custom blog templates and themes
- 🔗 **v2.4** - CMS integration (WordPress, Ghost, Notion)

## 🤝 Contributing

We welcome contributions! The new project structure makes it easy to contribute to specific components:

```bash
# Setup development environment
make setup

# Choose your area of contribution
make cli               # CLI improvements
make backend           # Backend API development  
make frontend          # Frontend development

# Run quality checks before submitting
make precommit
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact & Documentation

- 📧 **Email:** support@BlogTubeAI.com
- 💬 **Discord:** [BlogTubeAI Community](https://discord.gg/BlogTubeAI)
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/BlogTubeAI/issues)
- 📖 **Full Documentation:**
  - [CLI Guide](docs/cli-guide.md)
  - [Backend API Docs](backend/README.md)
  - [Frontend Guide](frontend/README.md)
  - [Development Guide](docs/development.md)

---

<div align="center">

**Made with ❤️ by the BlogTubeAI Team**

[⭐ Star us on GitHub](https://github.com/yourusername/BlogTubeAI) | [🐦 Follow on Twitter](https://twitter.com/BlogTubeAI) | [📧 Newsletter](https://newsletter.BlogTubeAI.com)

</div>

