# JobInsight AI

## Vision

JobInsight AI est une plateforme SaaS d'analyse du marché de l'emploi.

L'objectif est de collecter des offres d'emploi, extraire les compétences recherchées, analyser les tendances du marché et fournir des recommandations personnalisées aux utilisateurs.

---

## Stack Technique

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Redis
* Celery

### IA / NLP

* spaCy
* Sentence Transformers
* Gemini
* Qdrant

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Shadcn UI
* React Query
* Zustand

### Infrastructure

* Docker
* Docker Compose

---

## Fonctionnalités Principales

1. Collecte d'offres d'emploi
2. Extraction automatique des compétences
3. Analyse des tendances
4. Matching CV ↔ offres
5. Assistant IA de carrière
6. Dashboard analytique
7. Génération de rapports

---

## Agents Métier

* CollectorAgent
* SkillExtractionAgent
* TrendAnalysisAgent
* CVMatchingAgent
* CareerAdvisorAgent
* ReportAgent

Les agents métier sont implémentés dans le backend Python.

---

## Architecture

Frontend (Next.js)
↓
FastAPI
↓
Services
↓
Repositories
↓
PostgreSQL / Qdrant

Respecter :

* Clean Architecture
* SOLID
* Domain Driven Design
* Type Hints
* Pydantic v2
* Tests automatisés

---

## Priorités

1. Architecture maintenable
2. Code modulaire
3. APIs documentées
4. Séparation des responsabilités
5. Performance et scalabilité
6. UX moderne
