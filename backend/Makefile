# Backend Makefile
PROJECT_NAME := BlogTubeAI-Backend

# Directories
SRC_DIR := src
TEST_DIR := tests
CORE_DIR := src/core

.PHONY: help
help:
	@echo "$(PROJECT_NAME) - Backend Commands"
	@echo ""
	@echo "Development:"
	@echo "  setup         : Setup backend development environment"
	@echo "  run-dev       : Run FastAPI development server"
	@echo "  run-cli       : Run CLI application"
	@echo ""
	@echo "Testing:"
	@echo "  test          : Run all backend tests"
	@echo "  test-core     : Run core module tests"
	@echo "  test-web      : Run web API tests"
	@echo "  test-coverage : Run tests with coverage"

# =============================================================================
# Setup & Installation
# =============================================================================

.PHONY: setup
setup:
	@echo "Setting up backend environment..."
	pip install -r requirements.txt
	@echo "✅ Backend setup complete!"

# =============================================================================
# Development
# =============================================================================

.PHONY: run-dev
run-dev:
	@echo "Starting FastAPI development server..."
	uvicorn src.web.app:app --reload --host 0.0.0.0 --port 8000

.PHONY: run-cli
run-cli:
	@echo "Starting CLI application..."
	cd .. && python main.py --interactive

# =============================================================================
# Testing
# =============================================================================

.PHONY: test
test:
	@echo "Running all backend tests..."
	python -m pytest $(TEST_DIR) -v

.PHONY: test-core
test-core:
	@echo "Running core module tests..."
	python -m pytest $(TEST_DIR)/test_core -v

.PHONY: test-web
test-web:
	@echo "Running web API tests..."
	python -m pytest $(TEST_DIR)/test_web -v

.PHONY: test-coverage
test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest --cov=$(SRC_DIR) --cov-report=html $(TEST_DIR) -v

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: format
format:
	@echo "Formatting code..."
	black $(SRC_DIR) $(TEST_DIR) --line-length 88

.PHONY: lint
lint:
	@echo "Running linter..."
	flake8 $(SRC_DIR) $(TEST_DIR) --max-line-length=88
