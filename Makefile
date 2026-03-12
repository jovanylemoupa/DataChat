.PHONY: help install up down restart logs shell-backend shell-frontend migrate seed test pull-ollama

help:
	@echo ""
	@echo "  DataChat — Commandes disponibles"
	@echo "  ────────────────────────────────────────────────"
	@echo "  make install        Initialise le projet (1ère fois)"
	@echo "  make up             Lance tous les services"
	@echo "  make down           Arrête tous les services"
	@echo "  make restart        Redémarre tous les services"
	@echo "  make logs           Affiche les logs en temps réel"
	@echo "  make migrate        Lance les migrations Django"
	@echo "  make seed           Lance les seeders"
	@echo "  make test           Lance tous les tests"
	@echo "  make test-ai        Lance les évaluations LangSmith"
	@echo "  make shell-backend  Ouvre un shell dans le backend"
	@echo "  make pull-ollama    Télécharge le modèle Mistral"
	@echo "  ────────────────────────────────────────────────"
	@echo ""

# ── INITIALISATION ────────────────────────────────────────
install:
	docker compose build
	docker compose up -d postgres redis
	ping -n 6 127.0.0.1 > nul
	docker compose run --rm backend python manage.py migrate
	docker compose up -d
	make pull-ollama
	@echo "Projet initialise. Acces : http://localhost:4200"

# ── SERVICES ──────────────────────────────────────────────
up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down && docker compose up -d

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-celery:
	docker compose logs -f celery

# ── DJANGO ────────────────────────────────────────────────
migrate:
	docker compose run --rm backend python manage.py migrate

makemigrations:
	docker compose run --rm backend python manage.py makemigrations

seed:
	docker compose run --rm backend python scripts/run_seeders.py

shell-backend:
	docker compose exec backend bash

shell-django:
	docker compose exec backend python manage.py shell

# ── FRONTEND ──────────────────────────────────────────────
shell-frontend:
	docker compose exec frontend sh

# ── TESTS ─────────────────────────────────────────────────
test:
	docker compose run --rm backend pytest tests/unit tests/integration -v

test-ai:
	docker compose run --rm backend python interfaces/cli/run_evaluations.py

# ── OLLAMA ────────────────────────────────────────────────
pull-ollama:
	@echo "Téléchargement du modèle Mistral (peut prendre quelques minutes)..."
	docker compose exec ollama ollama pull mistral

# ── NETTOYAGE ─────────────────────────────────────────────
clean:
	docker compose down -v --remove-orphans
	@echo "⚠️  Tous les volumes supprimés"