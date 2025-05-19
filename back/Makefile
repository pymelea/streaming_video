# Makefile for Stream API Fast project

.PHONY: help install dev run test test-cov clean lint format seed seed-spiderman seed-underworld seed-blade seed-percy-jackson seed-all

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
UVICORN := $(POETRY) run uvicorn
PYTEST := $(POETRY) run pytest
FLAKE8 := $(POETRY) run flake8
BLACK := $(POETRY) run black

# Default port
PORT ?= 8000

# Help command
help:
	@echo "Available commands:"
	@echo "  make install       - Install project dependencies"
	@echo "  make dev           - Install development dependencies"
	@echo "  make run           - Run server in development mode"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean temporary files"
	@echo "  make seed          - Run legacy seed scripts to populate the database"
	@echo "  make seed-spiderman - Seed Spider-Man collection"
	@echo "  make seed-underworld - Seed Underworld collection"
	@echo "  make seed-blade    - Seed Blade collection"
	@echo "  make seed-percy-jackson - Seed Percy Jackson collection"
	@echo "  make seed-all      - Seed all movie collections"
	@echo "  make help          - Show this help"

# Install dependencies
install:
	$(POETRY) install --no-dev

# Install development dependencies
dev:
	$(POETRY) install

# Run server
run:
	$(UVICORN) main:app --reload --host 0.0.0.0 --port $(PORT)

# Run tests
test:
	$(PYTEST) tests/test_videos.py tests/test_subtitles.py tests/test_categories.py -v

# Run tests with coverage
test-cov:
	$(PYTEST) --cov=routers --cov=models tests/test_videos.py tests/test_subtitles.py tests/test_categories.py -v --cov-report=term --cov-report=html

# Run linter
lint:
	$(FLAKE8) .

# Format code
format:
	$(BLACK) .

# Clean temporary files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run legacy seed scripts
seed:
	$(PYTHON) -m seeds.seed_videos
	$(PYTHON) -m seeds.seed_playlists

# Run Spider-Man collection seed script
seed-spiderman:
	$(PYTHON) -m seeds.seed_collection

# Run Underworld collection seed script
seed-underworld:
	$(PYTHON) -m seeds.seed_underworld

# Run Blade collection seed script
seed-blade:
	$(PYTHON) -m seeds.seed_blade

# Run Percy Jackson collection seed script
seed-percy-jackson:
	$(PYTHON) -m seeds.seed_percy_jackson

# Run all collection seed scripts
seed-all:
	$(PYTHON) -m seeds.seed_all

