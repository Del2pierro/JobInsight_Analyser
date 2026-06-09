"""
Remotive Scraper — Public API Client
====================================
Analogie : Au lieu d'essayer de décoder la vitrine cryptée et surveillée (LinkedIn HTML),
on demande directement au gérant le catalogue au format numérique propre (Remotive API).

Flux technique :
1. On interroge l'API Remotive avec le mot-clé de recherche.
2. L'API retourne un JSON propre de toutes les offres correspondantes.
3. On filtre optionnellement par localisation (ex: "France" ou "Europe").
4. On mappe les objets JSON vers notre format standardisé ScrapedJob.
"""

import logging
from typing import List
import requests

from app.scrapers.base_scraper import BaseScraper, ScrapedJob

logger = logging.getLogger(__name__)


class RemotiveScraper(BaseScraper):
    """
    Scraper utilisant l'API publique et gratuite de Remotive pour récupérer des offres d'emploi.
    """

    REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

    def __init__(self):
        super().__init__(source_name="remotive")

    def scrape(
        self, keywords: str, location: str, num_pages: int = 3
    ) -> List[ScrapedJob]:
        """
        Interroge l'API Remotive et convertit les résultats en ScrapedJob.
        
        Note : Comme l'API retourne toutes les offres d'un coup, num_pages sert
        à limiter le volume d'offres récupérées (ex: 15 offres par page simulée).
        """
        self.logger.info(f"🔍 Recherche d'offres sur Remotive pour : '{keywords}' (Localisation: '{location}')")
        
        params = {"search": keywords}
        try:
            response = requests.get(self.REMOTIVE_API_URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'appel à l'API Remotive : {e}")
            return []

        jobs_list = data.get("jobs", [])
        self.logger.info(f"📊 {len(jobs_list)} offres brutes récupérées depuis Remotive.")

        scraped_jobs: List[ScrapedJob] = []
        limit = num_pages * 15  # Simulation de pagination

        for item in jobs_list:
            if len(scraped_jobs) >= limit:
                break

            # Filtrage par localisation si demandé
            job_location = item.get("candidate_required_location", "Worldwide")
            if location and location.strip().lower() not in job_location.lower():
                # On ignore l'offre si la localisation ne correspond pas
                continue

            # Mappage du type de contrat (Remotive renvoie des chaînes comme 'full_time', 'contract')
            contract_mapping = {
                "full_time": "CDI",
                "contract": "Freelance",
                "part_time": "Temps partiel",
                "internship": "Stage"
            }
            raw_type = item.get("job_type", "")
            contract_type = contract_mapping.get(raw_type, "CDI" if "full" in raw_type else raw_type)

            # Création de l'offre standardisée
            scraped_jobs.append(
                ScrapedJob(
                    title=item.get("title", "Offre sans titre"),
                    company=item.get("company_name", "Entreprise inconnue"),
                    location=job_location,
                    description=item.get("description", ""),  # HTML text
                    url=item.get("url", ""),
                    source="remotive",
                    contract_type=contract_type,
                    posted_date=item.get("publication_date"),
                    tags=item.get("tags", [])
                )
            )

        self._log_summary(scraped_jobs)
        return scraped_jobs
