# Documentation Technique - JobInsight AI

## 1. Philosophie de l'Architecture

### Clean Architecture
Le code est organisé en couches concentriques. La règle d'or est que les dépendances pointent toujours vers l'intérieur (le Domaine).
- **Couche Entités** : Contient les objets métier de base (`Job`, `Resume`, `Skill`).
- **Couche Cas d'Utilisation** : Implémentée via les **Agents**. Chaque agent a une responsabilité unique.
- **Couche Adaptateurs** : Routes FastAPI, schémas Pydantic.

---

## 2. Les Agents IA

L'intelligence du système est répartie entre plusieurs agents autonomes :

### CollectorAgent
- **Rôle** : Récupérer des offres d'emploi.
- **Technologie** : Scrapers (Remotive, etc.) + Celery pour le background.
- **Output** : Offres brutes en base de données.

### SkillExtractionAgent (NLP)
- **Rôle** : Lire la description des offres et extraire les compétences.
- **Technologie** : spaCy avec modèle français + Taxonomie personnalisée.
- **Process** : Normalisation des termes (ex: "JS" -> "JavaScript").

### MatcherAgent (Vector Search)
- **Rôle** : Calculer la compatibilité entre un CV et des offres.
- **Technologie** : **Qdrant**.
- **Mécanisme** : Les offres et les CV sont transformés en vecteurs (embeddings) de 384 dimensions. La recherche se fait par similarité cosinus.

---

## 3. Déploiement & DevOps

### Pipeline de Production
1. **Nginx** : Reçoit les requêtes HTTP/HTTPS sur le port 80/443.
2. **Frontend** : Container Next.js optimisé en "Static Export" ou "Node Runtime".
3. **Backend** : Container FastAPI servi par **Gunicorn** (4 workers).
4. **Workers Celery** : Gèrent les tâches lourdes (Scraping, NLP) pour ne pas bloquer l'API.

### Sécurité
- Les secrets sont chargés via `.env.prod`.
- Le réseau Docker `jobinsight_net` isole les bases de données de l'extérieur.
- JWT est utilisé pour l'authentification des utilisateurs.

---

## 4. Guide des API (v1)

### Jobs
- `GET /api/v1/jobs/` : Liste des offres (paginée).
- `POST /api/v1/jobs/scrape` : Lance une tâche de scraping.

### Resumes
- `POST /api/v1/resumes/` : Upload d'un CV PDF et extraction immédiate.

### Matching
- `GET /api/v1/matching/{resume_id}` : Récupère les meilleures offres pour un CV donné.

---

## 5. Maintenance & Monitoring
- **Logs** : Accessibles via `docker logs -f jobinsight_backend_prod`.
- **Base de données** : Backups conseillés sur le volume `pgdata_prod`.
- **Mise à jour** : Utiliser `./deploy.sh` qui automatise le cycle `pull -> build -> restart`.
