---
name: nextjs-frontend
description: Build modular, type-safe, and high-performance user interfaces using Next.js.
---
# Next.js Frontend

## Objectif
Développer l'interface utilisateur web avec Next.js de manière rapide, typée et fluide.

## Responsabilités
- Structurer l'application avec Next.js App Router.
- Intégrer les points d'API du backend de manière asynchrone.
- Garantir le typage strict des données entrantes.

## Bonnes Pratiques
- **RSC (Server Components)** : Rendre la majorité des composants côté serveur pour réduire le JavaScript client.
- **Client Boundary** : Déclarer `'use client'` le plus bas possible dans l'arborescence des composants.
- **Data Fetching** : Centraliser les appels d'API dans un client d'API dédié typé en TypeScript.

## Conventions
- Fichiers de composants en PascalCase (ex: `JobCard.tsx`).
- Typer chaque réponse d'API via des interfaces ou des types TypeScript clairs.
