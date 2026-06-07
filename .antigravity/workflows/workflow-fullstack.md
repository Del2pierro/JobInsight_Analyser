# Workflow Full Stack - JobInsight AI

## Objectif
Orchestrer le développement d'une fonctionnalité complète impliquant le domaine métier, l'API backend et l'interface utilisateur frontend, de manière cohérente et synchronisée.

## Agents impliqués
- **Software Architect Agent** : Design et découpage fonctionnel.
- **Backend Engineer Agent** : API, base de données, logique métier.
- **NLP Engineer Agent** : Pipeline NLP si extraction de texte requise.
- **Frontend Engineer Agent** : Composants et intégration API.
- **UI/UX Design Agent** : Expérience utilisateur et design.
- **QA Reviewer Agent** : Revue transversale avant merge.

## Diagramme

```mermaid
flowchart TD
    A([🚀 Nouvelle Feature Full Stack]) --> B[Software Architect Agent\nDécoupe en Use Cases + contrats API\nDéfinit les DTOs partagés]

    B --> C{NLP requis ?}
    C -- Oui --> D[NLP Engineer Agent\nPipeline d'extraction\nspaCy + embeddings]
    C -- Non --> E

    D --> E[Backend Engineer Agent\nImplémente les Use Cases\nCrée les endpoints FastAPI]

    E --> F[Backend Engineer Agent\nPersistence PostgreSQL\nIndexation Qdrant]

    F --> G[UI/UX Design Agent\nMaquette des écrans\nSpécifie les états UI]

    G --> H[Frontend Engineer Agent\nImplémente les composants\nNext.js + TypeScript]

    H --> I[Frontend Engineer Agent\nIntègre les appels API\nTypage des réponses]

    I --> J[QA Reviewer Agent\nRevue globale :\nBackend + NLP + Frontend]

    J --> K{Revue OK ?}
    K -- CRITIQUE Backend --> E
    K -- CRITIQUE Frontend --> H
    K -- AVERTISSEMENT --> L[Corrections mineures]
    L --> J
    K -- OK --> M[Tests end-to-end]
    M --> N([✅ Feature complète et mergée])
```

## Checklist
- [ ] Use Cases définis et validés par l'Architect
- [ ] Contrat API (schémas Pydantic) défini AVANT le code frontend
- [ ] Pipeline NLP intégré si requis
- [ ] Tests unitaires Backend écrits
- [ ] Composants Frontend typés
- [ ] Tests E2E couvrant le flux principal
- [ ] Revue QA passée sans critique bloquante
