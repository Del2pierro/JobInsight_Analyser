# Workflow Frontend - JobInsight AI

## Objectif
Développer un nouveau composant ou une nouvelle page dans l'interface Next.js, depuis la maquette jusqu'au composant typé et intégré.

## Agents impliqués
- **UI/UX Design Agent** : Conception et spécification du composant.
- **Frontend Engineer Agent** : Implémentation React / Next.js.
- **QA Reviewer Agent** : Revue du code et de l'accessibilité.

## Diagramme

```mermaid
flowchart TD
    A([🖥️ Nouveau composant / page]) --> B[UI/UX Design Agent\nSpécifie les états UI\ndefault, loading, empty, error]
    B --> C[UI/UX Design Agent\nDéfinit les props du composant\net les interactions utilisateur]
    C --> D[Frontend Engineer Agent\nDétermine Server vs Client Component]
    D --> E{Interactif / Stateful ?}
    E -- Oui --> F[Frontend Engineer Agent\nCrée un Client Component\navec use client]
    E -- Non --> G[Frontend Engineer Agent\nCrée un Server Component\ndata fetching côté serveur]
    F --> H[Frontend Engineer Agent\nType les props et les réponses API\nTypeScript strict]
    G --> H
    H --> I[Frontend Engineer Agent\nIntègre Tailwind + shadcn/ui\nrespect du Design System]
    I --> J[Frontend Engineer Agent\nAjoute skeleton loader\npour états de chargement]
    J --> K[QA Reviewer Agent\nRevue TypeScript, accessibilité\net performance]
    K --> L{Revue OK ?}
    L -- Non --> I
    L -- Oui --> M([✅ Composant prêt])
```

## Checklist
- [ ] États UI spécifiés (default, loading, empty, error)
- [ ] Boundary Server/Client Component définie
- [ ] Props typées en TypeScript (no `any`)
- [ ] Skeleton loader implémenté
- [ ] Classes Tailwind uniquement (pas de CSS custom)
- [ ] Variables shadcn/ui utilisées pour les couleurs
- [ ] Responsive (mobile, tablet, desktop)
- [ ] ARIA labels sur les éléments interactifs
