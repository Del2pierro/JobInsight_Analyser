# Workflow Deployment - JobInsight AI

## Objectif
Garantir un déploiement sûr, reproductible et sans régression de JobInsight AI, de la validation locale à la mise en production via Docker.

## Agents impliqués
- **DevOps Agent** : Build Docker, orchestration et configuration des services.
- **QA Reviewer Agent** : Validation pre-deploy (sécurité, healthchecks).
- **Backend Engineer Agent** : Validation des migrations de base de données.

## Diagramme

```mermaid
flowchart TD
    A([🐳 Déploiement requis]) --> B[QA Reviewer Agent\nAudit final du code\nSécurité + dette technique]
    B --> C{Critique bloquant ?}
    C -- Oui --> D[Correction avant déploiement\nRetour au workflow concerné]
    D --> B
    C -- Non --> E[Backend Engineer Agent\nValide les migrations Alembic\npendantes]
    E --> F{Migrations sûres ?}
    F -- Non --> G[Backup PostgreSQL\navant toute migration destructive]
    G --> H[Application des migrations\nen staging d'abord]
    F -- Oui --> H
    H --> I[DevOps Agent\nBuild des images Docker\nmulti-stage]
    I --> J[DevOps Agent\nVérifie les Dockerfiles\nnon-root, secrets via ENV]
    J --> K[DevOps Agent\nLance docker-compose\navec healthchecks]
    K --> L{Tous les services UP ?}
    L -- Non --> M[DevOps Agent\nDiagnostique les logs\ndes conteneurs en erreur]
    M --> I
    L -- Oui --> N[Smoke Tests\nValidation des endpoints critiques]
    N --> O{Smoke Tests OK ?}
    O -- Non --> P[Rollback\nRevenir à l'image précédente]
    P --> D
    O -- Oui --> Q([✅ Déploiement réussi])
```

## Checklist
- [ ] Revue QA sans critique bloquante
- [ ] Migrations Alembic relues et validées
- [ ] Backup PostgreSQL effectué si migrations destructives
- [ ] Images Docker buildées avec tag versionné (ex: `v1.2.0`)
- [ ] Secrets injectés via variables d'environnement (jamais hardcodés)
- [ ] Healthchecks configurés pour Postgres, Qdrant et API
- [ ] Smoke tests passés sur les endpoints critiques
- [ ] Plan de rollback documenté et testé
