.PHONY: help setup install install-dev install-web install-test clean build run run-dev run-prod test test-unit test-integration test-coverage lint format check migrate seed docker-build docker-run docker-stop logs

# Default target
help:
	@echo "BlogTubeAI Backend - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup         : Complete development environment setup"
	@echo "  install       : Install production dependencies"
	@echo "  install-dev   : Install development dependencies"
	@echo "  install-web   : Install web-specific dependencies"
	@echo "  install-test  : Install testing dependencies"
	@echo ""
	@echo "Development Commands:"
	@echo "  run           : Run development server with auto-reload"
	@echo "  run-dev       : Run development server (alias for run)"
	@echo "  run-prod      : Run production server"
	@echo "  build         : Build application for production"
	@echo ""
	@echo "Database Commands:"
	@echo "  migrate       : Run database migrations"
	@echo "  migrate-auto  : Auto-generate migration from models"
	@echo "  migrate-down  : Rollback last migration"
	@echo "  seed          : Seed database with test data"
	@echo "  db-reset      : Reset database (drop and recreate)"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test          : Run all tests"
	@echo "  test-unit     : Run unit tests only"
	@echo "  test-integration : Run integration tests only"
	@echo "  test-coverage : Run tests with coverage report"
	@echo "  test-watch    : Run tests in watch mode"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  lint          : Run code linting (flake8, mypy)"
	@echo "  format        : Format code (black, isort)"
	@echo "  check         : Run all code quality checks"
	@echo "  pre-commit    : Run pre-commit hooks"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build  : Build Docker images"
	@echo "  docker-run    : Run application in Docker"
	@echo "  docker-stop   : Stop Docker containers"
	@echo "  docker-logs   : View Docker logs"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean         : Clean temporary files and caches"
	@echo "  logs          : View application logs"
	@echo "  shell         : Start interactive Python shell"
	@echo "  docs          : Generate API documentation"

# Environment setup
setup: clean install-dev migrate seed
	@echo "✅ Development environment setup complete!"
	@echo "Run 'make run' to start the development server"

# Installation targets
install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/dev.txt

install-web:
	pip install -r requirements/web.txt

install-test:
	pip install -r requirements/test.txt

# Development server
run: run-dev

run-dev:
	@echo "🚀 Starting development server..."
	python scripts/start_dev.py

run-prod:
	@echo "🚀 Starting production server..."
	uvicorn src.web.app:app --host 0.0.0.0 --port 8000 --workers 4

# Build for production
build:
	@echo "🔨 Building application for production..."
	python -m compileall src/
	@echo "✅ Build complete!"

# Database operations
migrate:
	@echo "🗄️  Running database migrations..."
	python scripts/migrate.py

migrate-auto:
	@echo "🗄️  Auto-generating migration..."
	alembic revision --autogenerate -m "Auto migration"

migrate-down:
	@echo "🗄️  Rolling back last migration..."
	alembic downgrade -1

seed:
	@echo "🌱 Seeding database with test data..."
	python scripts/seed_data.py

db-reset:
	@echo "🗄️  Resetting database..."
	rm -f data/app.db
	python scripts/migrate.py
	python scripts/seed_data.py

# Testing
test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/integration/ -v

test-coverage:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v
	@echo "📊 Coverage report generated in htmlcov/"

test-watch:
	@echo "🧪 Running tests in watch mode..."
	pytest-watch tests/ -- -v

# Code quality
lint:
	@echo "🔍 Running linters..."
	flake8 src/ tests/
	mypy src/

format:
	@echo "🎨 Formatting code..."
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

check: lint
	@echo "✅ Code quality check complete!"

pre-commit:
	@echo "🔧 Running pre-commit hooks..."
	pre-commit run --all-files

# Docker operations
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-run:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d

docker-stop:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "🐳 Viewing Docker logs..."
	docker-compose logs -f

# Utility commands
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

logs:
	@echo "📋 Viewing application logs..."
	tail -f logs/app.log

shell:
	@echo "🐍 Starting interactive Python shell..."
	python -c "from src.web.app import app; import IPython; IPython.embed()"

docs:
	@echo "📚 Generating API documentation..."
	python scripts/generate_docs.py
	@echo "📖 Documentation available at http://localhost:8000/docs"

# Development helpers
dev-status:
	@echo "📊 Development Status:"
	@echo "  Python Version: $(shell python --version)"
	@echo "  Virtual Environment: $(shell echo $$VIRTUAL_ENV)"
	@echo "  Dependencies installed: $(shell pip list | wc -l) packages"
	@echo "  Database status: $(shell [ -f data/app.db ] && echo "Present" || echo "Missing")"
	@echo "  Test status: $(shell pytest tests/ --collect-only -q 2>/dev/null | tail -1 || echo "Not configured")"

dev-reset: clean db-reset
	@echo "🔄 Development environment reset complete!"
