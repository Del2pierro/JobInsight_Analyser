# 🚀 JobInsight AI

JobInsight AI est une plateforme SaaS de pointe pour l'analyse du marché de l'emploi, propulsée par une architecture multi-agents et des technologies NLP avancées.

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Next.js](https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

## 🌟 Vision
L'objectif de JobInsight AI est de transformer la recherche d'emploi et l'analyse de marché en fournissant des données exploitables :
- **Collecte intelligente** : Scraping automatisé d'offres tech.
- **Extraction NLP** : Identification automatique des compétences (Hard/Soft skills).
- **Matching Sémantique** : Score de compatibilité entre CV (PDF) et offres via Vector Search.
- **Analyse de Tendances** : Visualisation de l'évolution des salaires et des technologies.

---

## 🏗️ Architecture
Le projet suit les principes de la **Clean Architecture** et du **Domain-Driven Design (DDD)**.

### Backend (Python/FastAPI)
- **Domain** : Entités métier pures, sans dépendances techniques.
- **Application** : Orchestration via des Agents spécialisés (Collector, Extractor, Matcher, etc.).
- **Infrastructure** : PostgreSQL (données), Qdrant (recherche vectorielle), Redis (tâches Celery).

### Frontend (Next.js/TypeScript)
- Interface moderne avec **Tailwind CSS** et **Shadcn UI**.
- Dashboard analytique interactif.

---

## 🛠️ Stack Technique
- **Backend** : FastAPI, SQLAlchemy, Alembic, Celery, Pydantic v2.
- **IA/NLP** : spaCy, Sentence-Transformers (Embeddings), Google Gemini (Orchestration).
- **Bases de données** : PostgreSQL (Relationnel), Qdrant (Vectoriel), Redis (Queue).
- **Frontend** : Next.js 14 (App Router), TypeScript, Lucide React, Recharts.

---

## 🚀 Installation Rapide

### Prérequis
- Docker & Docker Compose
- Une clé API Google Gemini (optionnel, pour l'orchestrateur IA)

### Développement
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-repo/jobinsight-ai.git
   cd jobinsight-ai
   ```
2. Configurez le fichier `.env` dans le dossier `backend/`.
3. Lancez les services :
   ```bash
   docker compose up --build
   ```
L'application est disponible sur `http://localhost:3000`.

### Production (VM)
1. Utilisez le script de déploiement automatique :
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
2. Configurez votre `.env.prod` à partir de `.env.prod.example`.

---

## 📂 Structure du Projet
```
.
├── backend/               # FastAPI + Celery + IA
│   ├── app/
│   │   ├── agents/        # Logique des Agents IA
│   │   ├── domain/        # Entités pures (DDD)
│   │   ├── services/      # Qdrant, NLP, LLM
│   │   └── api/           # Routes v1
├── frontend/              # Next.js + Tailwind
├── docker-compose.yml     # Config Dev
├── docker-compose.prod.yml# Config Prod (Gunicorn + Nginx)
└── nginx.conf             # Reverse Proxy Prod
```

---

## 📄 Licence
Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

---
*Développé avec ❤️ par l'équipe JobInsight AI.*
