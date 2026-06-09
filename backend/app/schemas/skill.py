from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SkillBase(BaseModel):
    name: str
    category: str  # hard, soft

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobSkillBase(BaseModel):
    job_id: UUID
    skill_id: UUID
    weight: float = 1.0

class JobSkillOut(JobSkillBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
