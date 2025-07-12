# YouTube to Blog Converter - Makefile
PROJECT_NAME := BlobTubeAI

# Python and pip commands
PYTHON := python3
PIP := pip

# Requirement files
REQ := requirements.txt
REQ_IN := requirements.in
DEV_REQ := requirements-dev.txt
DEV_REQ_IN := requirements-dev.in

# Directories
SRC_DIR := src
TEST_DIR := tests
OUTPUT_DIR := output
LOGS_DIR := logs
TRANSCRIPTS_DIR := transcripts

# Default target
.PHONY: help
help:
	@echo "$(PROJECT_NAME) - YouTube to Blog Converter"
	@echo ""
	@echo "Available targets:"
	@echo "  Setup & Installation:"
	@echo "    install           Install production dependencies"
	@echo "    dev-install       Install development dependencies"
	@echo "    setup             Complete development setup"
	@echo "    install-tools     Install pip-tools for dependency management"
	@echo ""
	@echo "  Dependencies:"
	@echo "    deps              Compile requirements.txt from requirements.in"
	@echo "    dev-deps          Compile requirements-dev.txt from requirements-dev.in"
	@echo "    upgrade-deps      Upgrade all dependencies"
	@echo "    sync              Sync environment with compiled requirements"
	@echo ""
	@echo "  Code Quality:"
	@echo "    format            Run code formatter (black)"
	@echo "    lint              Run linter (flake8)"
	@echo "    type-check        Run type checker (mypy)"
	@echo "    check-all         Run all code quality checks"
	@echo ""
	@echo "  Testing:"
	@echo "    test              Run all tests"
	@echo "    test-unit         Run unit tests only"
	@echo "    test-integration  Run integration tests only"
	@echo "    test-coverage     Run tests with coverage report"
	@echo "    test-html         Generate HTML coverage report"
	@echo ""
	@echo "  Application:"
	@echo "    run               Run the main application interactively"
	@echo "    demo              Run demo with sample video"
	@echo "    example           Run with example YouTube URL"
	@echo ""
	@echo "  Maintenance:"
	@echo "    clean             Remove cache and temporary files"
	@echo "    clean-all         Remove all generated files including output"
	@echo "    logs              Show recent logs"
	@echo "    version           Show version information"
	@echo "    check-env         Check environment setup"

# =============================================================================
# Setup & Installation
# =============================================================================

.PHONY: install-tools
install-tools:
	@echo "Installing pip-tools for dependency management..."
	$(PIP) install pip-tools

.PHONY: deps
deps: install-tools
	@echo "Compiling production requirements..."
	pip-compile $(REQ_IN) --output-file $(REQ)

.PHONY: dev-deps
dev-deps: install-tools
	@echo "Compiling development requirements..."
	pip-compile $(DEV_REQ_IN) --output-file $(DEV_REQ)

.PHONY: compile-all
compile-all: deps dev-deps
	@echo "All requirements compiled!"

.PHONY: install
install: deps
	@echo "Installing production dependencies..."
	$(PIP) install -r $(REQ)

.PHONY: dev-install
dev-install: dev-deps
	@echo "Installing development dependencies..."
	$(PIP) install -r $(DEV_REQ)
	$(PIP) install -r $(REQ)

.PHONY: sync
sync: compile-all
	@echo "Syncing environment with compiled requirements..."
	pip-sync $(REQ) $(DEV_REQ)

.PHONY: setup
setup: create-dirs dev-install
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		echo "# API Keys - Add your keys here" > .env; \
		echo "OPENAI_API_KEY=your_openai_key_here" >> .env; \
		echo "ANTHROPIC_API_KEY=your_claude_key_here" >> .env; \
		echo "GOOGLE_API_KEY=your_gemini_key_here" >> .env; \
		echo "# Azure OpenAI (optional)" >> .env; \
		echo "AZURE_OPENAI_API_KEY=" >> .env; \
		echo "AZURE_OPENAI_ENDPOINT=" >> .env; \
		echo "AZURE_OPENAI_DEPLOYMENT_NAME=" >> .env; \
		echo ".env file created. Please add your API keys."; \
	fi
	@echo "Development environment setup complete!"
	@echo "Run 'make check-env' to verify setup"

# =============================================================================
# Dependencies Management
# =============================================================================

.PHONY: upgrade-deps
upgrade-deps: install-tools
	@echo "Upgrading all dependencies..."
	pip-compile --upgrade $(REQ_IN) --output-file $(REQ)
	pip-compile --upgrade $(DEV_REQ_IN) --output-file $(DEV_REQ)

.PHONY: add-dep
add-dep:
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make add-dep PACKAGE=package-name"; \
		exit 1; \
	fi
	@echo "Adding $(PACKAGE) to requirements.in..."
	@echo "$(PACKAGE)" >> $(REQ_IN)
	@make deps

.PHONY: add-dev-dep
add-dev-dep:
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make add-dev-dep PACKAGE=package-name"; \
		exit 1; \
	fi
	@echo "Adding $(PACKAGE) to requirements-dev.in..."
	@echo "$(PACKAGE)" >> $(DEV_REQ_IN)
	@make dev-deps

# =============================================================================
# Code Quality
# =============================================================================

.PHONY: format
format:
	@echo "Formatting code with black..."
	black $(SRC_DIR) $(TEST_DIR) main.py --line-length 88

.PHONY: format-check
format-check:
	@echo "Checking code formatting..."
	black $(SRC_DIR) $(TEST_DIR) main.py --check --line-length 88

.PHONY: lint
lint:
	@echo "Running linter (flake8)..."
	flake8 $(SRC_DIR) $(TEST_DIR) main.py --max-line-length=88 --extend-ignore=E203,W503

.PHONY: type-check
type-check:
	@echo "Running type checker (mypy)..."
	mypy $(SRC_DIR) main.py --ignore-missing-imports --strict-optional

.PHONY: check-all
check-all: format-check lint type-check
	@echo "All code quality checks completed!"

# =============================================================================
# Testing
# =============================================================================

.PHONY: test
test:
	@echo "Running all tests..."
	pytest $(TEST_DIR) -v --tb=short

.PHONY: test-unit
test-unit:
	@echo "Running unit tests..."
	pytest $(TEST_DIR) -v -k "not integration and not e2e" --tb=short

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	pytest $(TEST_DIR) -v -k "integration or e2e" --tb=short

.PHONY: test-coverage
test-coverage:
	@echo "Running tests with coverage..."
	pytest --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=xml $(TEST_DIR) -v

.PHONY: test-html
test-html:
	@echo "Generating HTML coverage report..."
	pytest --cov=$(SRC_DIR) --cov-report=html $(TEST_DIR)
	@echo "Coverage report generated at htmlcov/index.html"

.PHONY: test-watch
test-watch:
	@echo "Running tests in watch mode..."
	pytest-watch $(TEST_DIR) -- -v

# =============================================================================
# Application
# =============================================================================

.PHONY: run
run:
	@echo "Starting YouTube to Blog Converter in interactive mode..."
	$(PYTHON) main.py --interactive

.PHONY: demo
demo:
	@echo "Running demo with Rick Astley video..."
	$(PYTHON) main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --provider openai

.PHONY: example
example:
	@echo "Running with example TED Talk..."
	$(PYTHON) main.py "https://www.youtube.com/watch?v=f84n5oFoZBc" --language en --provider openai

.PHONY: quick-test
quick-test:
	@echo "Quick test with a short video..."
	$(PYTHON) main.py --interactive

# =============================================================================
# Maintenance
# =============================================================================

.PHONY: create-dirs
create-dirs:
	@echo "Creating project directories..."
	@mkdir -p $(OUTPUT_DIR) $(LOGS_DIR) $(TRANSCRIPTS_DIR) $(TEST_DIR)

.PHONY: clean
clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true
	rm -rf .tox/ 2>/dev/null || true

.PHONY: clean-all
clean-all: clean
	@echo "Removing all generated files..."
	rm -rf $(OUTPUT_DIR)/* 2>/dev/null || true
	rm -rf $(LOGS_DIR)/* 2>/dev/null || true
	rm -rf $(TRANSCRIPTS_DIR)/* 2>/dev/null || true

.PHONY: logs
logs:
	@echo "Recent application logs:"
	@if [ -d $(LOGS_DIR) ]; then \
		find $(LOGS_DIR) -name "*.log" -type f -exec ls -lt {} + | head -5; \
		echo ""; \
		echo "Latest log entries:"; \
		find $(LOGS_DIR) -name "*.log" -type f -exec tail -20 {} + 2>/dev/null | tail -20 || echo "No logs found"; \
	else \
		echo "No logs directory found. Run the application first."; \
	fi

.PHONY: version
version:
	@echo "$(PROJECT_NAME) Version Information:"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo "Working Directory: $(shell pwd)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "Git Commit: $(shell git rev-parse --short HEAD 2>/dev/null || echo 'Not a git repository')"

.PHONY: check-env
check-env:
	@echo "Checking environment setup..."
	@echo "Python version:"
	@$(PYTHON) -c "import sys; print(f'  {sys.version}')"
	@echo ""
	@echo "API Keys configured:"
	@$(PYTHON) -c "import os; keys = [('OpenAI', os.getenv('OPENAI_API_KEY')), ('Anthropic', os.getenv('ANTHROPIC_API_KEY')), ('Google', os.getenv('GOOGLE_API_KEY'))]; [print(f'  {k}: {\"✓\" if v else \"✗\"}') for k,v in keys]"
	@echo ""
	@echo "Required packages:"
	@$(PYTHON) -c "import importlib; packages = ['youtube_transcript_api', 'openai', 'click', 'rich', 'requests', 'dotenv']; [print(f'  {pkg.replace(\"_\", \"-\")}: ✓') if importlib.util.find_spec(pkg) else print(f'  {pkg.replace(\"_\", \"-\")}: ✗') for pkg in packages]" 2>/dev/null
	@echo ""
	@echo "Project directories:"
	@ls -la $(SRC_DIR) $(OUTPUT_DIR) $(LOGS_DIR) 2>/dev/null || echo "  Some directories missing - run 'make create-dirs'"

.PHONY: doctor
doctor: check-env
	@echo ""
	@echo "System Health Check:"
	@echo "Network connectivity:"
	@ping -c 1 api.openai.com >/dev/null 2>&1 && echo "  OpenAI API: ✓" || echo "  OpenAI API: ✗"
	@ping -c 1 youtube.com >/dev/null 2>&1 && echo "  YouTube: ✓" || echo "  YouTube: ✗"

# =============================================================================
# Development workflow shortcuts
# =============================================================================

.PHONY: dev
dev: setup check-env
	@echo ""
	@echo "Development environment ready! 🚀"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Add your API keys to .env file"
	@echo "  2. Run 'make run' to start the application"
	@echo "  3. Run 'make test' to run the test suite"

.PHONY: ci
ci: check-all test-coverage
	@echo "CI pipeline completed successfully! ✅"

.PHONY: precommit
precommit: format lint test-unit
	@echo "Pre-commit checks completed! ✅"

.PHONY: deploy-check
deploy-check: check-all test-coverage
	@echo "Deployment readiness check completed! 🚀"

# =============================================================================
# Quick start commands
# =============================================================================

.PHONY: init
init: create-dirs compile-all setup
	@echo "Project initialized successfully!"
	@echo "Run 'make doctor' to verify everything is working"

.PHONY: update
update: upgrade-deps sync
	@echo "Dependencies updated and synced!"

.PHONY: reset
reset: clean-all dev-install
	@echo "Environment reset complete!"
