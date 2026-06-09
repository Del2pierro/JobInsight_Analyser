#!/bin/bash

echo "🚀 Démarrage du déploiement JobInsight AI..."

# 1. Récupérer la dernière version du code
git pull origin main

# 2. Stopper et supprimer les anciens containers (optionnel selon ton flux)
# docker compose -f docker-compose.prod.yml down

# 3. Build et relance en arrière-plan
docker compose -f docker-compose.prod.yml up --build -d

# 4. Nettoyage des images inutilisées
docker image prune -f

echo "✅ Déploiement terminé !"
echo "📊 État des containers :"
docker compose -f docker-compose.prod.yml ps
