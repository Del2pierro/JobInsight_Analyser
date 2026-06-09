from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.core.exceptions import NotFoundException
from app.models.job import Job
from app.models.skill import Skill, JobSkill
from app.schemas.skill import SkillOut, JobSkillOut

router = APIRouter()


@router.get("/", response_model=List[SkillOut])
def list_skills(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[Skill]:
    """
    Get a list of all skills registered in the system.
    """
    skills = db.query(Skill).offset(skip).limit(limit).all()
    return skills


@router.get("/job/{job_id}", response_model=List[JobSkillOut])
def get_skills_by_job(
    job_id: str,
    db: Session = Depends(deps.get_db),
) -> List[JobSkill]:
    """
    Retrieve all skills required for a specific job along with their weights.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundException("Job", job_id)

    job_skills = db.query(JobSkill).filter(JobSkill.job_id == job_id).all()
    return job_skills
