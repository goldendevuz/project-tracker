.PHONY: help build up down logs shell db-migrate db-downgrade clean

help:
	@echo "Available commands:"
	@echo "  make build          - Build Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View logs from all services"
	@echo "  make logs-backend   - View backend logs"
	@echo "  make logs-db        - View database logs"
	@echo "  make shell          - Open bash shell in backend container"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make db-migrate     - Run database migrations"
	@echo "  make db-downgrade   - Downgrade database migrations"
	@echo "  make restart        - Restart all services"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost"
	@echo "Admin Panel: http://localhost/admin"
	@echo "API Docs: http://localhost/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-db:
	docker-compose logs -f db

shell:
	docker-compose exec backend bash

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

db-migrate:
	docker-compose exec backend alembic upgrade head

db-downgrade:
	docker-compose exec backend alembic downgrade -1

restart: down up
	@echo "Services restarted!"

ps:
	docker-compose ps

status:
	@echo "Checking service status..."
	@docker-compose ps
	@echo "\nAPI Health:"
	@curl -s http://localhost/health | jq . || echo "API not responding"
