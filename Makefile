.PHONY: help setup install test run debug clean lint format

help:
	@echo "Cab Navigation System - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Setup project (install deps, create venv)"
	@echo "  make install        - Install dependencies only"
	@echo ""
	@echo "Running:"
	@echo "  make run            - Run the CLI application"
	@echo "  make debug          - Run with debug mode enabled"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linting checks"
	@echo "  make format         - Format code (black)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Clean cache and build files"
	@echo "  make requirements   - Update requirements.txt"
	@echo ""
	@echo "Device:"
	@echo "  make devices        - List connected Android devices"
	@echo "  make logcat         - Show device logs"
	@echo ""

setup:
	@echo "🚗 Setting up Cab Navigation System..."
	bash setup.sh

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "🚀 Starting Cab Navigation System..."
	python main.py

debug:
	@echo "🐛 Starting with debug mode..."
	CAB_NAV_DEBUG=true LOG_LEVEL=DEBUG python main.py

test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v --tb=short 2>/dev/null || echo "pytest not installed. Install with: pip install pytest"

lint:
	@echo "🔍 Running linter..."
	python -m pylint agents/ models/ tools/ orchestrator.py config.py 2>/dev/null || echo "pylint not installed. Install with: pip install pylint"

format:
	@echo "✨ Formatting code..."
	python -m black agents/ models/ tools/ orchestrator.py config.py main.py 2>/dev/null || echo "black not installed. Install with: pip install black"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .pylint.d 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info 2>/dev/null || true
	echo "✓ Cleaned"

requirements:
	@echo "📝 Updating requirements.txt..."
	pip freeze | grep -E "droidrun|pydantic|llama-index|python-dotenv|aiohttp|requests" > requirements.txt
	echo "✓ Updated"

devices:
	@echo "📱 Connected Android devices:"
	adb devices -l

logcat:
	@echo "📋 Device logs (Press Ctrl+C to stop):"
	adb logcat

.env:
	@echo "📝 Creating .env file..."
	cp .env.example .env
	@echo "⚠️  Update .env with your API keys"

.DEFAULT_GOAL := help
