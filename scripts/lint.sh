#!/bin/bash

# Exit on error
set -e

# Run formatters
echo "Running black..."
black .

echo "Running isort..."
isort .

# Run linters
echo "Running flake8..."
flake8 .

echo "Running mypy..."
mypy .

# Run security checks
echo "Running bandit..."
bandit -r intelliagent/

echo "All checks passed!"
