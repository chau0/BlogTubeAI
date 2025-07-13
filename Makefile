# YouTube to Blog Converter - Project Makefile
PROJECT_NAME := BlogTubeAI

# Default target
.PHONY: help
help:
	@echo "$(PROJECT_NAME) - YouTube to Blog Converter"
	@echo ""
	@echo "Project Structure:"
	@echo "  CLI Application (root)"
	@echo "  Backend API (backend/)"
	@echo "  Frontend React App (frontend/)"
	@echo ""
	@echo "Available targets:"
	@echo "  🚀 Quick Start:"
	@echo "    setup             Complete project setup"
	@echo "    dev               Start development environment"
	@echo "    test-all          Run all tests across project"
	@echo ""
	@echo "  📁 Component Commands:"
	@echo "    cli               CLI application commands"
	@echo "    backend           Backend API commands"
	@echo "    frontend          Frontend application commands"
	@echo ""
	@echo "  🧹 Maintenance:"
	@echo "    clean             Clean all components"
	@echo "    check-env         Check entire project environment"

# =============================================================================
# Project-wide commands
# =============================================================================

.PHONY: setup
setup:
	@echo "Setting up complete BlogTubeAI project..."
	@$(MAKE) -C backend setup
	@$(MAKE) -C frontend install
	@echo "✅ Project setup complete!"

.PHONY: dev
dev:
	@echo "Starting development environment..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:5173"
	@$(MAKE) -C backend run-dev &
	@$(MAKE) -C frontend dev

.PHONY: test-all
test-all:
	@echo "Running all tests..."
	@$(MAKE) -C backend test
	@$(MAKE) -C frontend test

.PHONY: clean
clean:
	@echo "Cleaning entire project..."
	@$(MAKE) -C backend clean
	@$(MAKE) -C frontend clean
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# =============================================================================
# CLI Commands (for backward compatibility)
# =============================================================================

.PHONY: cli cli-run cli-demo cli-test
cli:
	@echo "CLI Commands:"
	@echo "  cli-run     : Run CLI interactively"
	@echo "  cli-demo    : Run CLI demo"
	@echo "  cli-test    : Test CLI functionality"

cli-run:
	@echo "Starting CLI application..."
	python main.py --interactive

cli-demo:
	@echo "Running CLI demo..."
	python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --provider openai

cli-test:
	@$(MAKE) -C backend test-core

# =============================================================================
# Component delegation
# =============================================================================

.PHONY: backend
backend:
	@echo "Backend commands - run 'make -C backend help' for details"
	@$(MAKE) -C backend help

.PHONY: frontend  
frontend:
	@echo "Frontend commands - run 'make -C frontend help' for details"
	@$(MAKE) -C frontend help

# =============================================================================
# Environment checking
# =============================================================================

.PHONY: check-env
check-env:
	@echo "Checking project environment..."
	@python --version
	@node --version 2>/dev/null || echo "Node.js not installed"
	@$(MAKE) -C backend check-env
