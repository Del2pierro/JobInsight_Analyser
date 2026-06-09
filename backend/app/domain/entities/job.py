from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Optional
from app.domain.entities.skill import Skill

@dataclass
class Job:
    """
    Pure Domain Entity representing a Job Offer.
    """
    title: str
    description: str
    company_name: str
    id: UUID = field(default_factory=uuid4)
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "EUR"
    job_type: Optional[str] = None # CDI, CDD, etc.
    experience_level: Optional[str] = None
    raw_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    skills: List[Skill] = field(default_factory=list)

    def add_skill(self, skill: Skill):
        if skill not in self.skills:
            self.skills.append(skill)
