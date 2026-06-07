# Workflow Analytics - JobInsight AI

## Objectif
Ajouter une nouvelle analyse de données ou visualisation du marché de l'emploi, depuis la préparation des données jusqu'à l'affichage frontend.

## Agents impliqués
- **Data Scientist Agent** : Préparation et agrégation des données.
- **Backend Engineer Agent** : Exposition des données via un endpoint API.
- **Data Visualization Agent** : Conception et intégration du graphique.
- **UI/UX Design Agent** : Cohérence visuelle et états de chargement.

## Diagramme

```mermaid
flowchart TD
    A([📊 Nouveau besoin analytique]) --> B[Data Scientist Agent\nIdentifie les données sources\net les métriques à calculer]
    B --> C[Data Scientist Agent\nNettoie et agrège les données\nvia Pandas vectorisé]
    C --> D{Données fiables\net cohérentes ?}
    D -- Non --> E[Data Scientist Agent\nDiagnostique et corrige\nla qualité des données]
    E --> C
    D -- Oui --> F[Backend Engineer Agent\nCrée l'endpoint API FastAPI\nRéponse typée Pydantic]
    F --> G[Data Visualization Agent\nChoisit le type de graphique adapté\nex: BarChart, LineChart, Heatmap]
    G --> H[Data Visualization Agent\nImplémente avec Recharts\ndans le composant Next.js]
    H --> I[UI/UX Design Agent\nValide la cohérence visuelle\nAjoute skeleton loader]
    I --> J{UX validée ?}
    J -- Non --> H
    J -- Oui --> K[QA Reviewer Agent\nRevue code et accessibilité]
    K --> L([✅ Visualisation déployée])
```

## Checklist
- [ ] Sources de données identifiées (PostgreSQL / Pandas)
- [ ] Opérations Pandas vectorisées (pas de `iterrows`)
- [ ] Endpoint API typé avec Pydantic Response
- [ ] Type de graphique adapté aux données (max 6 couleurs)
- [ ] Skeleton loader défini pour l'état de chargement
- [ ] Tooltips et labels ARIA accessibles
- [ ] Mode sombre / clair validé
