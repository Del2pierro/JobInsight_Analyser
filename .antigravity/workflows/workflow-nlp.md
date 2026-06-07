# Workflow NLP - JobInsight AI

## Objectif
Orchestrer l'ajout ou l'amélioration d'un composant de traitement du langage naturel, de l'extraction d'entités jusqu'à l'indexation vectorielle.

## Agents impliqués
- **NLP Engineer Agent** : Configuration spaCy et extraction des entités.
- **Data Scientist Agent** : Validation et évaluation de la qualité.
- **Backend Engineer Agent** : Intégration dans le service FastAPI.
- **Qdrant RAG Engineer (Skill)** : Indexation des vecteurs produits.

## Diagramme

```mermaid
flowchart TD
    A([🧠 Nouveau besoin NLP]) --> B[NLP Engineer Agent\nDéfinit les entités à extraire\nex: SKILL, ROLE, SECTOR]
    B --> C[NLP Engineer Agent\nConfigure SpanRuler / Matcher spaCy]
    C --> D[NLP Engineer Agent\nTest sur corpus de validation]
    D --> E{Précision suffisante ?\nF1 > 0.80}
    E -- Non --> F[NLP Engineer Agent\nAjuste les règles / patterns]
    F --> D
    E -- Oui --> G[Data Scientist Agent\nValide la distribution des extractions\nsur le jeu de données complet]
    G --> H{Distribution cohérente ?}
    H -- Non --> F
    H -- Oui --> I[Backend Engineer Agent\nIntègre le pipeline dans\napp/services/nlp_service.py]
    I --> J[Backend Engineer Agent\nExposes les résultats via API]
    J --> K[Qdrant RAG Engineer\nGénère les embeddings\net indexe dans Qdrant]
    K --> L[QA Reviewer Agent\nRevue du code et des tests]
    L --> M([✅ Pipeline NLP en production])
```

## Checklist
- [ ] Entités cibles définies (noms en MAJUSCULES)
- [ ] Modèle spaCy chargé en Singleton dans `app/core/nlp.py`
- [ ] Composants inutilisés désactivés (`disable=[]`)
- [ ] Traitement en lot via `nlp.pipe()`
- [ ] F1 > 0.80 sur corpus de validation
- [ ] Service NLP intégré dans `app/services/`
- [ ] Vecteurs indexés dans Qdrant avec payload structuré
