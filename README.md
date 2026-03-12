# DataChat — Agent IA d'analyse de documents conversationnel

Stack : Angular 17 · PrimeNG · Django 5 · Pandas · NumPy · LangChain · LangGraph · Keycloak · LangSmith · Ollama

---

## Prérequis

- Docker Desktop (WSL2 activé sur Windows)
- Node.js 20+
- Angular CLI : `npm install -g @angular/cli`
- Git

---

## Démarrage rapide

```bash
# 1. Cloner le repo
git clone <url-du-repo>
cd datachat

# 2. Initialiser le projet (première fois)
make install
# → copie .env.example → .env
# → build les images Docker
# → lance les migrations Django
# → télécharge Mistral via Ollama

# 3. Accès
# Frontend  : http://localhost:4200
# Backend   : http://localhost:8000/api/
# Keycloak  : http://localhost:8080  (admin / admin)
# ChromaDB  : http://localhost:8001
```

---

## Commandes utiles

```bash
make up             # Démarrer tous les services
make down           # Arrêter tous les services
make logs           # Voir les logs en temps réel
make migrate        # Lancer les migrations Django
make shell-backend  # Shell dans le container backend
make test           # Lancer les tests
make test-ai        # Lancer les évaluations LangSmith
```

---

## Structure du projet

```
datachat/
├── frontend/        # Angular 17 + PrimeNG
├── backend/         # Django 5 (Clean Architecture)
│   ├── domain/      # Entités métier pures
│   ├── application/ # Use cases
│   ├── infrastructure/ # Django ORM, LangGraph, ChromaDB
│   └── interfaces/  # API REST (controllers, serializers)
├── infra/           # Keycloak, Nginx, PostgreSQL
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## Variables d'environnement

Copier `.env.example` en `.env` et renseigner :
- `LANGCHAIN_API_KEY` — clé LangSmith (gratuit sur smith.langchain.com)
- `POSTGRES_USER` / `POSTGRES_PASSWORD`
- `KEYCLOAK_CLIENT_SECRET`

Le LLM utilisé est **Mistral via Ollama** (local, coût zéro).
