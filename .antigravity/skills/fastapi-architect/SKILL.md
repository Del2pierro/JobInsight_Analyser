---
name: fastapi-architect
description: Design and develop clean, high-performance FastAPI applications.
---
# FastAPI Architect

## Objectif
Concevoir des API robustes, performantes et structurées selon Clean Architecture et DDD.

## Responsabilités
- Structurer les points d'entrée API (routers, dépendances).
- Gérer la validation et sérialisation de données avec Pydantic v2.
- Configurer les middlewares (CORS, logs, sécurité).

## Bonnes Pratiques
- **I/O Asynchrones** : Routes asynchrones (`async def`) pour l'I/O.
- **Dependency Injection** : Utiliser `Depends` pour injecter les services et sessions de base de données.
- **Gestion des Erreurs** : Lever des exceptions HTTP au niveau de la couche d'interface, pas dans le domaine.

## Conventions
- Chemins d'API au format kebab-case.
- DTOs nommés avec suffixes `Request` ou `Response` (ex: `JobCreateRequest`).
