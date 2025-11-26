.PHONY: install test lint format clean build help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies using uv"
	@echo "  make test       - Run tests with pytest"
	@echo "  make lint       - Run ruff linter"
	@echo "  make format     - Format code with ruff"
	@echo "  make clean      - Remove build artifacts and cache"
	@echo "  make build      - Build the package"

install:
	uv pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src/prompt_groomer --cov-report=term-missing

lint:
	ruff check src/ tests/

format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	uv build
