"""
Celery Worker Configuration — JobInsight AI
=============================================
Point d'entrée unique pour la configuration Celery.

Ce fichier configure :
- Le broker Redis (file d'attente des tâches).
- Le backend Redis (stockage des résultats).
- L'auto-découverte des tâches dans app/tasks/.
- Le planning Celery Beat pour le scraping automatique.
"""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# ---------------------------------------------------------------------------
# Instance Celery
# ---------------------------------------------------------------------------

celery_app = Celery(
    "jobinsight_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.orchestrator_tasks",
        "app.tasks.scraping_tasks",
    ],
)

# ---------------------------------------------------------------------------
# Configuration du Worker
# ---------------------------------------------------------------------------

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_concurrency=2,
)

# ---------------------------------------------------------------------------
# Celery Beat Schedule — Scraping automatique planifié
# ---------------------------------------------------------------------------
# Analogie : C'est comme un réveil qui sonne toutes les 6 heures
# pour dire "Hey, c'est l'heure d'aller chercher les nouvelles offres !"
#
# L'utilisateur n'a RIEN à faire. Le système scrape tout seul.
# Les mots-clés et la localisation sont configurables via le .env
# ou via une table "search_queries" en base (future amélioration).
# ---------------------------------------------------------------------------

celery_app.conf.beat_schedule = {
    "scrape-jobs-periodically": {
        "task": "task_scrape_jobs",
        "schedule": crontab(
            minute=0,
            hour="*/6",  # Toutes les 6 heures (00:00, 06:00, 12:00, 18:00)
        ),
        "args": (
            settings.SCRAPE_DEFAULT_KEYWORDS,
            settings.SCRAPE_DEFAULT_LOCATION,
            settings.SCRAPING_DEFAULT_PAGES,
        ),
    },
}
