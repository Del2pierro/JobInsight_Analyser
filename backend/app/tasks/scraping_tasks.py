"""
Scraping Tasks — Tâches Celery asynchrones pour le scraping
===========================================================
Analogie : Tu passes commande au drive (l'API) → la cuisine (Celery)
prépare ton repas en arrière-plan → tu reçois une notification quand c'est prêt.

Ce fichier orchestre :
1. Réception de la demande de scraping.
2. Lancement du client API Remotive.
3. Sauvegarde des offres en base PostgreSQL.
4. Déclenchement du pipeline IA (extraction compétences + vectorisation).
"""

import logging
import uuid

from app.tasks.worker import celery_app

logger = logging.getLogger(__name__)


import asyncio

@celery_app.task(
    name="task_scrape_jobs",
    bind=True,
    max_retries=2,
    soft_time_limit=300,   # 5 minutes max
    time_limit=360,        # Kill dur à 6 minutes
)
def task_scrape_linkedin(
    self,
    keywords: str,
    location: str,
    num_pages: int = 3,
    user_id: str | None = None,
):
    """
    Tâche Celery qui lance la récupération d'offres via l'OrchestratorAgent.
    """
    logger.info(
        f"🚀 Démarrage de la récupération d'offres : "
        f"keywords='{keywords}', location='{location}'"
    )

    from app.agents.orchestrator import orchestrator_agent

    try:
        saved_count = asyncio.run(orchestrator_agent.collect_and_process(
            keywords=keywords,
            location=location
        ))
        return {
            "status": "completed",
            "jobs_saved": saved_count,
        }
    except Exception as e:
        logger.error(f"❌ Erreur lors du scraping : {e}")
        raise self.retry(exc=e, countdown=10)
