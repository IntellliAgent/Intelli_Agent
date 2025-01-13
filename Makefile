.PHONY: install test lint format clean docs

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	flake8 intelliagent tests
	mypy intelliagent tests
	black --check intelliagent tests
	isort --check-only intelliagent tests

format:
	black intelliagent tests
	isort intelliagent tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +

docs:
	sphinx-build -b html docs/source docs/build/html
