from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    """Base schema for Job shared properties."""
    title: str
    company: str
    location: Optional[str] = None
    description: str
    salary_range: Optional[str] = None
    contract_type: Optional[str] = None
    url: Optional[str] = None
    source: str = "manual"


class JobCreate(JobBase):
    """Schema for creating a new job."""
    pass


class JobOut(JobBase):
    """Schema for returning job data from the API."""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Schémas pour le Scraping ---

class ScrapeRequest(BaseModel):
    """Paramètres envoyés par le frontend pour lancer un scraping."""
    keywords: str           # ex: "Data Scientist", "Développeur React"
    location: str = "France"  # ex: "Paris", "Lyon", "Remote"
    num_pages: int = 3      # Nombre de pages LinkedIn à scraper (25 offres/page)


class ScrapeResponse(BaseModel):
    """Réponse immédiate avec l'ID de la tâche Celery pour le suivi."""
    task_id: str
    message: str
    status: str = "pending"
