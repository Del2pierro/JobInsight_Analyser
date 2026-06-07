---
name: docker-devops
description: Orchestrate containers, manage environments, and ensure reliable deployment pipelines using Docker.
---
# Docker DevOps

## Objectif
Garantir des environnements locaux et de production isolés, reproductibles et sécurisés.

## Responsabilités
- Écrire et optimiser les Dockerfiles (backend et frontend).
- Orchestrer les services (Postgres, Qdrant, API, Frontend) via Docker Compose.
- Gérer les volumes de persistance de données et les réseaux de conteneurs.

## Bonnes Pratiques
- **Multi-stage Build** : Limiter la taille des images finales en séparant les étapes de build et de run.
- **Non-root User** : Exécuter les processus dans les conteneurs sous un utilisateur système non-root.
- **Ordre des couches** : Copier d'abord les fichiers de dépendances (`requirements.txt`, `package.json`) pour exploiter le cache Docker.

## Conventions
- Utiliser des versions d'images de base explicites et légères (ex: `python:3.11-slim`, `node:20-alpine`).
- Centraliser les secrets et configurations dans des variables d'environnement (`.env`).
