# BlogTubeAI Backend

A FastAPI-based web backend for BlogTubeAI that provides RESTful APIs and WebSocket connections to support a modern React frontend while reusing the existing CLI functionality.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Management](#database-management)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Docker Development](#docker-development)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

The BlogTubeAI backend provides:

- **RESTful APIs** for video processing and job management
- **WebSocket connections** for real-time progress updates
- **Background job processing** for YouTube-to-blog conversion
- **Database persistence** for job tracking and history
- **Integration** with existing CLI modules
- **Security features** including rate limiting and input validation

### Key Features

- 🚀 **FastAPI** framework for high-performance async APIs
- 📊 **Real-time progress tracking** via WebSocket connections
- 🗄️ **SQLite/PostgreSQL** database with migrations
- 🔄 **Background job processing** with retry mechanisms
- 📝 **Comprehensive logging** and error handling
- 🛡️ **Security** with rate limiting and input validation
- 🧪 **Full test coverage** with unit and integration tests
- 🐳 **Docker support** for development and deployment

## Prerequisites

### System Requirements

- **Python 3.9+** (Python 3.11+ recommended)
- **pip** package manager
- **Git** for version control
- **Make** for build automation (optional but recommended)

### Optional Dependencies

- **Docker & Docker Compose** (for containerized development)
- **PostgreSQL** (for production database)
- **Redis** (for advanced caching, optional)

### Platform Support

- ✅ **Linux** (Ubuntu 20.04+, CentOS 8+)
- ✅ **macOS** (10.15+)
- ✅ **Windows** (Windows 10+ with WSL2 recommended)

## Quick Start

Get up and running in under 5 minutes:

```bash
# Clone the repository
git clone <repository-url>
cd BlogTubeAI/backend

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Complete setup (installs dependencies, sets up database, seeds test data)
make setup

# Start development server
make run

# Open your browser to http://localhost:8000/docs
```

That's it! The API documentation will be available at `http://localhost:8000/docs`.

## Development Setup

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.9+
```

### 2. Install Dependencies

```bash
# Install all development dependencies
make install-dev

# Or install manually:
pip install -r requirements/dev.txt

# For production only:
make install
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Required environment variables:

```bash
# Application Settings
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///./data/app.db

# API Keys (optional for development)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_AI_API_KEY=your-google-ai-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 4. Database Setup

```bash
# Run database migrations
make migrate

# Seed with test data
make seed

# Or do both at once:
make db-reset
```

### 5. Verify Installation

```bash
# Check development status
make dev-status

# Run basic health check
make test-unit
```

## Project Structure

```
backend/
├── src/                          # Source code
│   ├── web/                      # Web application layer
│   │   ├── app.py                # FastAPI application
│   │   ├── config.py             # Configuration
│   │   └── middleware/           # Custom middleware
│   ├── api/                      # API routes
│   │   ├── v1/                   # API version 1
│   │   └── websocket/            # WebSocket handlers
│   ├── core/                     # Business logic
│   │   ├── job_manager.py        # Job management
│   │   └── background_tasks.py   # Task processing
│   ├── models/                   # Data models
│   │   ├── database.py           # SQLAlchemy models
│   │   └── schemas.py            # Pydantic schemas
│   ├── services/                 # Service layer
│   ├── database/                 # Database operations
│   └── utils/                    # Utilities
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── fixtures/                 # Test data
├── requirements/                 # Dependencies
│   ├── base.txt                  # Core dependencies
│   ├── dev.txt                   # Development
│   ├── web.txt                   # Web-specific
│   └── test.txt                  # Testing
├── scripts/                      # Utility scripts
├── docker/                       # Docker configuration
├── data/                         # Application data
├── logs/                         # Log files
└── Makefile                      # Build automation
```

## Configuration

### Environment-Based Configuration

The application supports multiple environments:

- **development**: Local development with debug features
- **testing**: Test environment with in-memory database
- **production**: Production deployment with optimizations

### Key Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `src/web/config.py` | Application configuration |
| `alembic.ini` | Database migration config |
| `pyproject.toml` | Project metadata and tools |

### Configuration Options

```python
# Database
DATABASE_URL = "sqlite:///./data/app.db"  # Development
DATABASE_URL = "postgresql://user:pass@host:port/db"  # Production

# Security
SECRET_KEY = "your-secret-key"
CORS_ORIGINS = ["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE = 60
MAX_CONCURRENT_JOBS = 5

# File Storage
UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/outputs"
MAX_FILE_SIZE = 10485760  # 10MB
```

## Running the Application

### Development Server

```bash
# Start with auto-reload
make run

# Or directly with uvicorn
uvicorn src.web.app:app --reload --host 0.0.0.0 --port 8000
```

The development server includes:
- 🔄 **Auto-reload** on code changes
- 📊 **Debug logging** and error details
- 🌐 **CORS enabled** for frontend development
- 📖 **Interactive docs** at `/docs`

### Production Server

```bash
# Production mode
make run-prod

# Or with custom configuration
uvicorn src.web.app:app --host 0.0.0.0 --port 8000 --workers 4
```

Production features:
- ⚡ **Multiple workers** for better performance
- 🛡️ **Security hardening** and rate limiting
- 📈 **Performance optimizations**
- 📊 **Metrics and monitoring**

### Environment-Specific Commands

```bash
# Development
ENVIRONMENT=development make run

# Testing
ENVIRONMENT=testing make test

# Production
ENVIRONMENT=production make run-prod
```

## Database Management

### Migrations

```bash
# Run pending migrations
make migrate

# Create new migration
make migrate-auto

# Rollback last migration
make migrate-down

# Reset database completely
make db-reset
```

### Manual Migration Commands

```bash
# Check migration status
alembic current

# Create custom migration
alembic revision -m "Add new feature"

# Upgrade to specific revision
alembic upgrade head

# Downgrade to specific revision
alembic downgrade -1
```

### Database Operations

```bash
# Seed test data
make seed

# Backup database
cp data/app.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Database shell
sqlite3 data/app.db
```

## Testing

### Test Suite Overview

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints and responses
- **WebSocket Tests**: Test real-time functionality

### Running Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run with coverage
make test-coverage

# Watch mode for development
make test-watch

# Run specific test file
pytest tests/unit/test_job_manager.py -v

# Run tests matching pattern
pytest tests/ -k "test_video" -v
```

### Test Configuration

```bash
# Test environment variables
ENVIRONMENT=testing
DATABASE_URL=sqlite:///:memory:
TESTING=true

# Run tests with specific config
ENVIRONMENT=testing pytest tests/ -v
```

### Writing Tests

Example test structure:

```python
# tests/unit/test_job_service.py
import pytest
from unittest.mock import AsyncMock, patch

from src.services.job_service import JobService
from src.models.schemas import JobCreateRequest

@pytest.mark.asyncio
async def test_create_job_success():
    """Test successful job creation"""
    service = JobService()
    request = JobCreateRequest(
        video_url="https://youtube.com/watch?v=test",
        language_code="en",
        llm_provider="openai"
    )
    
    job = await service.create_job(request)
    
    assert job.status == "pending"
    assert job.video_url == request.video_url
```

### Test Coverage

```bash
# Generate coverage report
make test-coverage

# View coverage in browser
open htmlcov/index.html
```

Target coverage: **>90%** for all modules

## Code Quality

### Linting and Formatting

```bash
# Format code
make format

# Run linters
make lint

# Run all quality checks
make check

# Run pre-commit hooks
make pre-commit
```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style guide enforcement
- **mypy**: Static type checking
- **pytest**: Testing framework

### Pre-commit Hooks

Install pre-commit hooks for automatic quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### Code Style Guidelines

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Write **docstrings** for public methods
- Maintain **>90% test coverage**
- Use **meaningful variable names**

## Docker Development

### Docker Setup

```bash
# Build Docker images
make docker-build

# Start containers
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop
```

### Docker Compose Services

```yaml
# docker-compose.yml
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - ./src:/app/src
      - ./data:/app/data

  database:
    image: postgres:15
    environment:
      POSTGRES_DB: blogtubeai
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Development with Docker

```bash
# Start development environment
docker-compose up -d

# View backend logs
docker-compose logs -f backend

# Execute commands in container
docker-compose exec backend python scripts/migrate.py

# Rebuild after changes
docker-compose build backend
docker-compose up -d backend
```

## API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
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
