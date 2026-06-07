---
name: sqlalchemy-expert
description: Implement database access, models, and migrations using SQLAlchemy and Alembic.
---
# SQLAlchemy Expert

## Objectif
Interfacer l'application avec PostgreSQL via l'ORM SQLAlchemy de manière asynchrone et optimisée.

## Responsabilités
- Définir les modèles déclaratifs SQLAlchemy.
- Écrire des requêtes complexes en syntaxe SQLAlchemy 2.0.
- Gérer les migrations de schéma avec Alembic.

## Bonnes Pratiques
- **Syntaxe 2.0** : Utiliser `select()` et `session.execute()`. Pas d'utilisation de l'ancien style `session.query()`.
- **Problème N+1** : Charger explicitement les relations nécessaires avec `selectinload` ou `joinedload`.
- **Sessions** : Utiliser un scope de session asynchrone limité à la requête HTTP (`async_sessionmaker`).

## Conventions
- Modèles dans `app/models/` héritant d'une classe `Base` commune.
- Tout changement de schéma doit faire l'objet d'une migration Alembic relue manuellement.
