# Makefile for NUAA CLI - Auto-fixing and testing helpers
# Use 'make help' to see all available commands

.PHONY: help install install-dev format lint test test-cov security check fix all clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "NUAA CLI - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package only
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e .[dev]

format: ## Auto-format code with black and ruff
	@echo "🎨 Formatting code..."
	black src/nuaa_cli tests scripts/python
	ruff check --fix src/nuaa_cli tests scripts/python
	@echo "✅ Formatting complete!"

lint: ## Check code style without fixing
	@echo "🔍 Checking code style..."
	black --check src/nuaa_cli tests scripts/python
	ruff check src/nuaa_cli tests scripts/python

type-check: ## Run type checking with mypy
	@echo "🔎 Running type checks..."
	mypy src/nuaa_cli

test: ## Run tests
	@echo "🧪 Running tests..."
	pytest -q

test-cov: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	pytest
	@echo ""
	@echo "📊 Coverage report generated at htmlcov/index.html"

security: ## Run security scan with bandit
	@echo "🔒 Running security scan..."
	bandit -r src/nuaa_cli -f screen || true
	@echo "✅ Security scan complete!"

check: ## Run all checks (format, lint, type-check, security, test)
	@echo "🔍 Running all checks..."
	@$(MAKE) lint
	@$(MAKE) type-check
	@$(MAKE) security
	@$(MAKE) test
	@echo "✅ All checks passed!"

fix: ## Auto-fix all issues (format + security scan)
	@echo "🔧 Auto-fixing all issues..."
	@$(MAKE) format
	@$(MAKE) security
	@echo "✅ All fixes applied!"

ci: ## Run CI checks locally (same as GitHub Actions)
	@echo "🤖 Running CI checks locally..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) type-check
	python scripts/python/update_agents_docs.py
	@if ! git diff --quiet -- README.md AGENTS.md; then \
		echo "❌ Agent docs are out of date. Run 'python scripts/python/update_agents_docs.py'"; \
		git --no-pager diff README.md AGENTS.md; \
		exit 1; \
	fi
	python scripts/python/verify_agent_script_parity.py
	@$(MAKE) test-cov
	@$(MAKE) security
	@echo "✅ All CI checks passed!"

pre-commit: ## Install and run pre-commit hooks
	@echo "🪝 Setting up pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	pre-commit run --all-files
	@echo "✅ Pre-commit hooks installed!"

clean: ## Clean generated files
	@echo "🧹 Cleaning generated files..."
	rm -rf build/ dist/ *.egg-info .eggs/
	rm -rf htmlcov/ .coverage .coverage.* coverage.xml
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf .tox/ .bandit/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	@echo "✅ Cleanup complete!"

all: fix check ## Fix all issues and run all checks
	@echo "🚀 All done!"

# Quick shortcuts
f: format ## Shortcut for 'format'
l: lint ## Shortcut for 'lint'
t: test ## Shortcut for 'test'
tc: test-cov ## Shortcut for 'test-cov'
s: security ## Shortcut for 'security'
c: check ## Shortcut for 'check'
