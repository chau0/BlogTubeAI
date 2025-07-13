# BlogTubeAI Backend

The FastAPI-based backend for BlogTubeAI that provides RESTful APIs and WebSocket connections for the React frontend while reusing the proven CLI functionality through shared core modules.

## 📋 Overview

The BlogTubeAI backend serves as both:
- **API Server** for the React web interface with real-time progress tracking
- **Core Logic Provider** for the CLI application through shared modules
- **Job Processing Engine** for background YouTube-to-blog conversion

### 🏗️ Architecture Highlights

- 🚀 **FastAPI** framework for high-performance async APIs
- 📊 **Real-time progress tracking** via WebSocket connections  
- 🗄️ **SQLite/PostgreSQL** database with Alembic migrations
- 🔄 **Background job processing** with retry mechanisms
- 📝 **Comprehensive logging** and error handling
- 🛡️ **Security** with rate limiting and input validation
- 🧪 **Full test coverage** with unit and integration tests
- 🐳 **Docker support** for development and deployment

## 📁 Project Structure

```
backend/
├── src/
│   ├── core/                          # ✨ Core Business Logic (Migrated from Phase 1)
│   │   ├── youtube_parser.py          # YouTube URL parsing & video info
│   │   ├── transcript_handler.py      # Transcript fetching & processing  
│   │   ├── llm_providers.py           # AI provider integrations
│   │   ├── blog_formatter.py          # Markdown formatting & output
│   │   └── utils.py                   # Shared utility functions
│   │
│   ├── web/                           # FastAPI Web Application
│   │   ├── app.py                     # FastAPI application factory
│   │   ├── config.py                  # Configuration management
│   │   └── middleware/                # Custom middleware
│   │
│   ├── api/                           # REST API Endpoints
│   │   ├── v1/                        # API version 1
│   │   │   ├── videos.py              # Video processing endpoints
│   │   │   ├── jobs.py                # Job management endpoints
│   │   │   ├── providers.py           # LLM provider endpoints
│   │   │   └── health.py              # Health check endpoints
│   │   └── websocket/                 # WebSocket handlers
│   │
│   ├── models/                        # Data Models & Schemas
│   │   ├── database.py                # SQLAlchemy models
│   │   ├── schemas.py                 # Pydantic request/response models
│   │   └── enums.py                   # Enum definitions
│   │
│   ├── services/                      # Business Logic Services
│   │   ├── video_service.py           # Video processing service
│   │   ├── job_service.py             # Job management service
│   │   ├── provider_service.py        # LLM provider service
│   │   └── notification_service.py    # WebSocket notifications
│   │
│   ├── database/                      # Database Operations
│   │   ├── connection.py              # Database connection
│   │   └── repositories/              # Data access layer
│   │
│   └── utils/                         # Web-specific Utilities
│
├── tests/                             # Comprehensive Test Suite
│   ├── test_core/                     # ✨ Core Module Tests (Migrated)
│   │   ├── test_youtube_parser.py
│   │   ├── test_transcript_handler.py
│   │   ├── test_llm_providers.py
│   │   ├── test_blog_formatter.py
│   │   └── test_utils.py
│   ├── test_web/                      # Web API Tests
│   │   ├── test_api_endpoints.py
│   │   ├── test_websocket.py
│   │   └── test_job_workflow.py
│   ├── test_main.py                   # CLI Integration Tests
│   ├── conftest.py                    # Test configuration
│   └── fixtures/                      # Test data
│
├── requirements/                       # Dependency Management
│   ├── base.txt                       # Core dependencies
│   ├── web.txt                        # Web-specific dependencies
│   ├── dev.txt                        # Development dependencies
│   └── test.txt                       # Testing dependencies
│
├── scripts/                           # Utility Scripts
│   ├── start_dev.py                   # Development server
│   ├── migrate.py                     # Database migrations
│   └── seed_data.py                   # Test data generation
│
├── data/                              # Application Data
├── logs/                              # Log Files
├── output/                            # Generated Content
├── .env.example                       # Environment template
├── alembic.ini                        # Database migration config
├── Makefile                           # Development commands
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (Python 3.11+ recommended)
- **pip** package manager
- **SQLite** (included with Python) or **PostgreSQL** (optional)

### 1. Setup Backend Environment

```bash
# From project root
cd backend

# Setup backend development environment
make setup

# Or manual setup
pip install -r requirements/dev.txt
```

### 2. Configure Environment

```bash
# Create environment file from template
cp .env.example .env

# Edit with your API keys
nano .env
```

Required environment variables:
```env
# Development settings
ENVIRONMENT=development
DEBUG=True

# Database
DATABASE_URL=sqlite:///./data/app.db

# API Keys (choose at least one)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here
GOOGLE_API_KEY=your-gemini-key-here

# Azure OpenAI (optional)
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 3. Initialize Database

```bash
# Run database migrations
make migrate

# Seed with test data (optional)
make seed
```

### 4. Start Development Server

```bash
# Start FastAPI development server
make run-dev

# Server will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

## 🛠️ Development Commands

### **Core Development**
```bash
make help              # Show all available commands
make setup             # Complete development environment setup
make run-dev           # Start FastAPI development server
make run-cli           # Run CLI application (using shared core modules)
```

### **Testing**
```bash
make test              # Run all backend tests
make test-core         # Run core module tests (migrated from Phase 1)
make test-web          # Run web API tests
make test-coverage     # Run tests with coverage report
make test-watch        # Run tests in watch mode
```

### **Database Management**
```bash
make migrate           # Run pending database migrations
make migrate-auto      # Auto-generate migration from models
make migrate-down      # Rollback last migration
make seed              # Seed database with test data
make db-reset          # Reset database completely
```

### **Code Quality**
```bash
make format            # Format code with black
make lint              # Run linter (flake8)
make type-check        # Run type checker (mypy)
make check-all         # Run all code quality checks
```

### **Application Operations**
```bash
make logs              # View recent application logs
make shell             # Interactive Python shell with app context
make clean             # Clean cache and temporary files
```

## 🔧 API Documentation

### **REST API Endpoints**

The backend provides a comprehensive REST API for the frontend:

#### **Video Operations**
```
GET  /api/v1/videos/validate          # Validate YouTube URL
GET  /api/v1/videos/{video_id}/info   # Get video metadata
GET  /api/v1/videos/{video_id}/languages # Get available transcript languages
```

#### **Job Management**
```
POST   /api/v1/jobs/                  # Create new conversion job
GET    /api/v1/jobs/                  # List user jobs
GET    /api/v1/jobs/{job_id}          # Get job details
DELETE /api/v1/jobs/{job_id}          # Cancel/delete job
GET    /api/v1/jobs/{job_id}/download # Download job results
```

#### **Provider Management**
```
GET  /api/v1/providers/               # List available LLM providers
POST /api/v1/providers/validate       # Validate provider API keys
GET  /api/v1/providers/{provider}/status # Check provider health
```

#### **System Endpoints**
```
GET /health                           # Health check
GET /metrics                          # Application metrics
GET /docs                             # Interactive API documentation
```

### **WebSocket Endpoints**

Real-time communication for job progress:

```
WS /ws/jobs/{job_id}                  # Job progress updates
WS /ws/system                         # System-wide notifications
```

### **API Documentation**

When running the development server, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Database Schema

### **Job Tracking Tables**

```sql
-- Main jobs table
CREATE TABLE jobs (
    id TEXT PRIMARY KEY,              -- UUID
    video_id TEXT NOT NULL,           -- YouTube video ID
    video_url TEXT NOT NULL,          -- Original URL
    video_title TEXT,                 -- Video title
    language_code TEXT NOT NULL,      -- Transcript language
    llm_provider TEXT NOT NULL,       -- AI provider used
    status TEXT NOT NULL,             -- pending/processing/completed/failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    output_file_path TEXT,
    transcript_file_path TEXT
);

-- Job progress tracking
CREATE TABLE job_progress (
    job_id TEXT REFERENCES jobs(id),
    step TEXT NOT NULL,               -- validation/transcript/generation/formatting
    status TEXT NOT NULL,             -- pending/running/completed/failed
    message TEXT,                     -- Progress message
    progress_percentage INTEGER,      -- 0-100
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing Guide

### **Test Structure**

The backend includes comprehensive tests for both core logic and web functionality:

```bash
# Core module tests (migrated from Phase 1)
make test-core                        # All core module tests
pytest tests/test_core/test_youtube_parser.py -v
pytest tests/test_core/test_llm_providers.py -v

# Web API tests
make test-web                         # All web API tests  
pytest tests/test_web/test_api_endpoints.py -v
pytest tests/test_web/test_websocket.py -v

# Integration tests
pytest tests/test_main.py -v         # CLI integration tests
pytest tests/test_web/test_job_workflow.py -v # End-to-end job tests
```

### **Test Coverage Goals**

- 🎯 **Core Modules**: 95%+ coverage (migrated from Phase 1)
- 🎯 **Web APIs**: 90%+ coverage
- 🎯 **Integration**: 85%+ coverage
- 🎯 **Overall**: 90%+ coverage

### **Mocking and Fixtures**

Tests use comprehensive mocking for external services:

```python
# Example: Testing with mocked YouTube API
@patch('backend.src.core.youtube_parser.get_video_title')
def test_video_title_extraction(mock_get_title):
    mock_get_title.return_value = "Test Video Title"
    # Test implementation...
```

## 🔒 Security Features

### **API Security**
- **Rate Limiting**: Configurable per-endpoint rate limits
- **Input Validation**: Pydantic models for request validation
- **CORS Configuration**: Configurable cross-origin resource sharing
- **API Key Management**: Secure storage and validation of LLM provider keys

### **Data Protection**
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Automatic HTML escaping in responses
- **File Upload Security**: Validated file types and size limits
- **Environment Variables**: Sensitive data stored in environment variables

## 🚀 Deployment

### **Production Setup**

```bash
# Build for production
make build

# Set production environment
export ENVIRONMENT=production

# Start production server
make run-prod
```

### **Docker Deployment**

```bash
# Build Docker image
make docker-build

# Run with Docker Compose
make docker-run

# Or manually
docker run -p 8000:8000 --env-file .env blogtube-backend
```

### **Environment Configuration**

Production environment variables:
```env
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/blogtube
SECRET_KEY=your-production-secret-key
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🔧 Configuration

### **Environment-Based Configuration**

The application supports multiple environments:

- **development**: Local development with debug features
- **testing**: Test environment with in-memory database
- **production**: Production deployment with optimizations

### **Key Configuration Files**

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `src/web/config.py` | Application configuration |
| `alembic.ini` | Database migration config |
| `requirements/` | Dependency management |

## 🔍 Monitoring & Logging

### **Application Logs**

```bash
# View recent logs
make logs

# Follow logs in real-time
tail -f logs/backend_$(date +%Y-%m-%d).log

# Error logs only
grep ERROR logs/backend_*.log
```

### **Health Monitoring**

```bash
# Check application health
curl http://localhost:8000/health

# Get application metrics  
curl http://localhost:8000/metrics
```

## 🛠️ Troubleshooting

### **Common Issues**

**❌ "Module not found" errors after migration**
```bash
# Ensure you're in the backend directory
cd backend
python -c "from src.core.youtube_parser import get_video_id; print('✅ Imports working')"
```

**❌ "Database connection failed"**
```bash
# Check database file permissions
ls -la data/app.db

# Reset database if corrupted
make db-reset
```

**❌ "API key validation failed"**
```bash
# Check environment variables
make check-env

# Test API key manually
python -c "import openai; print('✅ OpenAI key valid')"
```

**❌ "Port already in use"**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### **Debug Mode**

```bash
# Run with debug logging
DEBUG=True make run-dev

# Interactive debugging
make shell
```

## 📈 Performance Optimization

### **Database Optimization**
- Connection pooling for concurrent requests
- Indexed columns for frequently queried fields
- Query optimization with SQLAlchemy lazy loading

### **API Performance**
- Async/await pattern for non-blocking operations
- Background task processing for long-running jobs
- Response caching for static data

### **Memory Management**
- Proper cleanup of temporary files
- Connection cleanup for external APIs
- Garbage collection optimization

## 🤝 Contributing to Backend

### **Development Setup**

```bash
# Setup development environment
make setup

# Install pre-commit hooks
pre-commit install

# Run tests before committing
make precommit
```

### **Code Style Guidelines**

- **PEP 8** compliance via black formatting
- **Type hints** for all function signatures
- **Docstrings** for all public functions and classes
- **Unit tests** for all new functionality

### **Pull Request Process**

1. Create feature branch from `main`
2. Implement changes with tests
3. Run quality checks: `make check-all`
4. Submit pull request with description

## 📧 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/BlogTubeAI/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/BlogTubeAI/discussions)
- 📖 **Documentation**: [Backend API Docs](http://localhost:8000/docs)
- 📧 **Email**: backend-support@BlogTubeAI.com

---

<div align="center">

**Backend built with ❤️ using FastAPI and Python**

[⭐ Star the Project](https://github.com/yourusername/BlogTubeAI) | [📖 Full Documentation](../README.md) | [🚀 Frontend Guide](../frontend/README.md)

</div>
- **OpenAPI Spec**: `http://localhost:8000/openapi.json`

### API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/videos/validate` | POST | Validate YouTube URL |
| `/api/v1/jobs` | POST | Create new job |
| `/api/v1/jobs/{id}` | GET | Get job status |
| `/api/v1/jobs/{id}` | DELETE | Cancel job |
| `/api/v1/providers` | GET | List LLM providers |
| `/api/v1/health` | GET | Health check |
| `/api/v1/ws/jobs/{id}` | WS | Real-time updates |

### Example API Usage

```bash
# Validate YouTube URL
curl -X POST "http://localhost:8000/api/v1/videos/validate" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=example"}'

# Create job
curl -X POST "http://localhost:8000/api/v1/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://youtube.com/watch?v=example",
    "language_code": "en",
    "llm_provider": "openai"
  }'

# Check job status
curl "http://localhost:8000/api/v1/jobs/{job_id}"
```

## Deployment

### Production Deployment

```bash
# Build for production
make build

# Install production dependencies only
make install

# Run production server
make run-prod
```

### Environment Variables for Production

```bash
# .env.production
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-production-secret-key

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
CORS_ORIGINS=["https://yourdomain.com"]
RATE_LIMIT_PER_MINUTE=30

# Monitoring
LOG_LEVEL=WARNING
METRICS_ENABLED=true
```

### Docker Production Deployment

```bash
# Build production image
docker build -f docker/Dockerfile.backend -t blogtubeai-backend .

# Run production container
docker run -d \
  --name blogtubeai-backend \
  -p 8000:8000 \
  --env-file .env.production \
  blogtubeai-backend
```

### Performance Considerations

- Use **PostgreSQL** for production database
- Configure **connection pooling** for database
- Set appropriate **worker count** based on CPU cores
- Enable **caching** with Redis for frequently accessed data
- Configure **rate limiting** based on expected load

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Problem: ModuleNotFoundError
# Solution: Ensure PYTHONPATH is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use development installation
pip install -e .
```

#### 2. Database Issues

```bash
# Problem: Database locked or corrupted
# Solution: Reset database
make db-reset

# Problem: Migration conflicts
# Solution: Check migration status and resolve
alembic current
alembic history
```

#### 3. Permission Errors

```bash
# Problem: Permission denied for data directory
# Solution: Fix permissions
chmod -R 755 data/
chown -R $USER:$USER data/
```

#### 4. Port Already in Use

```bash
# Problem: Port 8000 already in use
# Solution: Kill existing process or use different port
lsof -ti:8000 | xargs kill -9
# Or
uvicorn src.web.app:app --port 8001
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
make run

# Or set in .env file
echo "LOG_LEVEL=DEBUG" >> .env
```

### Performance Issues

```bash
# Check system resources
htop

# Monitor database queries
export DATABASE_ECHO=true

# Profile application
python -m cProfile -o profile.stats scripts/start_dev.py
```

### Getting Help

1. **Check logs**: `make logs` or `tail -f logs/app.log`
2. **Run diagnostics**: `make dev-status`
3. **Check GitHub Issues**: Search for similar problems
4. **Create detailed bug report** with:
   - Python version
   - Operating system
   - Error messages
   - Steps to reproduce

## Contributing

### Development Workflow

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** and add tests
4. **Run quality checks**: `make check`
5. **Run tests**: `make test`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push branch**: `git push origin feature/amazing-feature`
8. **Create Pull Request**

### Code Standards

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Use conventional commit messages

### Testing Requirements

- All new features must have tests
- Maintain >90% code coverage
- Include integration tests for API endpoints
- Test both success and error cases

---

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Support

- 📧 **Email**: [support@blogtubeai.com](mailto:support@blogtubeai.com)
- 💬 **GitHub Issues**: [Create an issue](https://github.com/yourusername/BlogTubeAI/issues)
- 📖 **Documentation**: [Full documentation](https://docs.blogtubeai.com)

---

**Made with ❤️ by the BlogTubeAI Team**
