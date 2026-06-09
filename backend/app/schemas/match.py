from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class MatchBase(BaseModel):
    resume_id: UUID
    job_id: UUID
    compatibility_score: float
    matched_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    feedback_rating: Optional[int] = None

class MatchCreate(MatchBase):
    pass

class MatchOut(MatchBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
