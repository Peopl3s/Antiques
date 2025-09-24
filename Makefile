.PHONY: help install install-dev lint lint-fix format type-check check test clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	uv sync

install-dev: ## Install development dependencies
	uv sync --dev

lint: ## Run linting with ruff
	uv run ruff check src/ tests/

lint-fix: ## Run linting with ruff and fix auto-fixable issues
	uv run ruff check --fix src/ tests/

format: ## Format code with ruff
	uv run ruff format src/ tests/

type-check: ## Run type checking with mypy
	uv run mypy src/

check: ## Run all checks (lint + format check + type check)
	uv run ruff check src/ tests/
	uv run ruff format --check src/ tests/
	uv run mypy src/

test: ## Run tests
	uv run pytest tests/ -v

test-cov: ## Run tests with coverage
	uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage

dev-setup: install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make check' to verify everything is working."

ci: check test ## Run CI pipeline (lint + type check + test)
	@echo "CI pipeline completed successfully!"
