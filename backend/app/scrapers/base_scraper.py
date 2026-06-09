"""
Base Scraper — Interface Abstraite
===================================
Analogie : C'est le « cahier des charges » d'une usine.
Toutes les usines (LinkedIn, Indeed, WTTJ) DOIVENT produire des pièces
au même format, peu importe leurs machines internes.

Ce fichier définit :
- Le format standard d'une offre scrapée (ScrapedJob).
- Le contrat que chaque scraper doit respecter (BaseScraper).
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ScrapedJob:
    """
    Représentation standardisée d'une offre d'emploi scrapée.
    Tous les scrapers DOIVENT convertir leurs données brutes vers ce format.
    """
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str  # "linkedin", "indeed", "wttj", etc.

    # Champs optionnels enrichis
    salary_range: Optional[str] = None
    contract_type: Optional[str] = None      # CDI, CDD, Freelance, Stage
    experience_level: Optional[str] = None   # Junior, Mid, Senior, Lead
    posted_date: Optional[str] = None
    tags: List[str] = field(default_factory=list)


class BaseScraper(ABC):
    """
    Classe abstraite pour tous les scrapers.
    Chaque nouveau site cible doit hériter de cette classe
    et implémenter la méthode `scrape()`.
    """

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.logger = logging.getLogger(f"scraper.{source_name}")

    @abstractmethod
    def scrape(self, keywords: str, location: str, num_pages: int = 3) -> List[ScrapedJob]:
        """
        Lance le scraping et retourne une liste d'offres standardisées.

        Args:
            keywords: Mots-clés de recherche (ex: "Data Scientist").
            location: Localisation (ex: "Paris", "France").
            num_pages: Nombre de pages de résultats à scraper.

        Returns:
            Liste de ScrapedJob normalisées.
        """
        ...

    def _log_summary(self, jobs: List[ScrapedJob]) -> None:
        """Log un résumé post-scraping pour le monitoring."""
        self.logger.info(
            f"[{self.source_name.upper()}] Scraping terminé : "
            f"{len(jobs)} offres collectées."
        )
