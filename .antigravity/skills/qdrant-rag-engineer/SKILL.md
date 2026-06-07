---
name: qdrant-rag-engineer
description: Implement vector indexing, search, and retrieval pipelines using Qdrant.
---
# Qdrant RAG Engineer

## Objectif
Permettre la recherche sémantique en indexant offres et profils sous forme de vecteurs dans Qdrant.

## Responsabilités
- Concevoir la structure des collections Qdrant (taille des vecteurs, métriques).
- Implémenter l'ingestion vectorielle en lot.
- Configurer les filtres de recherche hybrides.

## Bonnes Pratiques
- **Payload Filters** : Créer des index de payload sur les champs fréquemment filtrés (ex: `location`, `salary_min`).
- **Filtres natifs** : Combiner recherche vectorielle et filtres logiques directement dans la requête Qdrant.
- **Similarité** : Utiliser la similarité Cosinus par défaut pour la comparaison d'embeddings textuels.

## Conventions
- Associer les IDs des points Qdrant à des UUIDs générés à partir des IDs de la base PostgreSQL.
- Regrouper la logique client Qdrant dans un module dédié (ex: `app/core/qdrant.py`).
