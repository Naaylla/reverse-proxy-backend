.PHONY: help install test format lint type-check run-design run-assembly run-quality run-packaging docker-build docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make format        - Format code with black and isort"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make type-check    - Run mypy type checker"
	@echo "  make run-design    - Run design service"
	@echo "  make run-assembly  - Run assembly service"
	@echo "  make run-quality   - Run quality service"
	@echo "  make run-packaging - Run packaging service"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker Compose services"
	@echo "  make docker-down   - Stop Docker Compose services"
	@echo "  make clean         - Remove cache files"

install:
	pip install -r requirements.txt

test:
	pytest --cov=app --cov-report=html --cov-report=term-missing

format:
	black app/ tests/
	isort app/ tests/

lint:
	flake8 app/ tests/

type-check:
	mypy app/

run-design:
	uvicorn app.api.design_service:app --reload --port 8001

run-assembly:
	uvicorn app.api.assembly_service:app --reload --port 8002

run-quality:
	uvicorn app.api.quality_service:app --reload --port 8003

run-packaging:
	uvicorn app.api.packaging_service:app --reload --port 8004

docker-build:
	docker build -t assembly-factory .

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache
