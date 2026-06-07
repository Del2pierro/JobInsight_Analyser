# Workflow Backend - JobInsight AI

## Objectif
Guider le développement d'une nouvelle fonctionnalité API de bout en bout, depuis la définition du domaine jusqu'à la mise en production.

## Agents impliqués
- **Software Architect Agent** : Validation du design et du domaine.
- **Backend Engineer Agent** : Implémentation FastAPI / SQLAlchemy.
- **QA Reviewer Agent** : Revue et tests avant merge.

## Diagramme

```mermaid
flowchart TD
    A([🎯 Nouvelle Feature Backend]) --> B[Software Architect Agent\nDéfinit Entity / Value Object / Use Case]
    B --> C{Design validé ?}
    C -- Non --> B
    C -- Oui --> D[Backend Engineer Agent\nCrée le schéma Pydantic v2]
    D --> E[Backend Engineer Agent\nCrée le modèle SQLAlchemy]
    E --> F[Backend Engineer Agent\nGénère la migration Alembic]
    F --> G[Backend Engineer Agent\nImplémente le Use Case / Service]
    G --> H[Backend Engineer Agent\nCrée le router FastAPI + Depends]
    H --> I[QA Reviewer Agent\nRevue sécurité & respect Clean Arch]
    I --> J{Revue OK ?}
    J -- CRITIQUE --> G
    J -- AVERTISSEMENT --> K[Correction mineure]
    K --> I
    J -- OK --> L[Tests unitaires + intégration]
    L --> M([✅ Feature prête pour merge])
```

## Checklist
- [ ] Entity/Value Object définis dans `app/domain/`
- [ ] Use Case dans `app/application/`
- [ ] Schéma Pydantic Request/Response dans `app/schemas/`
- [ ] Modèle SQLAlchemy dans `app/models/`
- [ ] Migration Alembic générée et relue
- [ ] Router enregistré dans `app/api/`
- [ ] Tests écrits dans `tests/`
