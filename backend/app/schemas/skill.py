from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SkillBase(BaseModel):
    name: str
    category: str
    market_demand: float = 0.0
    is_normalized: bool = False

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id: UUID
    level: SkillLevel = SkillLevel.INTERMEDIATE  # Default level for display
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobSkillBase(BaseModel):
    job_id: UUID
    skill_id: UUID
    weight: float = 1.0

class JobSkillOut(JobSkillBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
