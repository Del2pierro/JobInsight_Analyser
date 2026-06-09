from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.entities.job import Job as DomainJob
from app.domain.entities.skill import Skill as DomainSkill
from app.domain.interfaces.repositories import JobRepository, SkillRepository
from app.models.job import Job as DBJob, Company as DBCompany
from app.models.skill import Skill as DBSkill

class SQLAlchemyJobRepository(JobRepository):
    """
    SQLAlchemy implementation of the JobRepository.
    Handles mapping between Domain Entities and Database Models.
    """
    def __init__(self, session: Session):
        self.session = session

    async def save(self, job: DomainJob) -> DomainJob:
        # Check if company exists or create it
        company = self.session.query(DBCompany).filter(DBCompany.name == job.company_name).first()
        if not company:
            company = DBCompany(name=job.company_name)
            self.session.add(company)
            self.session.flush()

        # Check if job exists by URL
        db_job = self.session.query(DBJob).filter(DBJob.raw_url == job.raw_url).first() if job.raw_url else None
        
        if not db_job:
            db_job = DBJob(
                id=job.id,
                company_id=company.id,
                title=job.title,
                description=job.description,
                location=job.location,
                salary_min=job.salary_min,
                salary_max=job.salary_max,
                salary_currency=job.salary_currency,
                job_type=job.job_type,
                experience_level=job.experience_level,
                raw_url=job.raw_url,
                created_at=job.created_at
            )
            self.session.add(db_job)
        else:
            # Update existing job
            db_job.title = job.title
            db_job.description = job.description
            db_job.location = job.location
            # ... other fields ...

        self.session.commit()
        return job

    async def get_by_id(self, job_id: UUID) -> Optional[DomainJob]:
        db_job = self.session.get(DBJob, job_id)
        if not db_job:
            return None
        return self._to_domain(db_job)

    async def get_by_url(self, url: str) -> Optional[DomainJob]:
        db_job = self.session.query(DBJob).filter(DBJob.raw_url == url).first()
        if not db_job:
            return None
        return self._to_domain(db_job)

    async def list_jobs(self, limit: int = 10, offset: int = 0) -> List[DomainJob]:
        db_jobs = self.session.query(DBJob).offset(offset).limit(limit).all()
        return [self._to_domain(db) for db in db_jobs]

    async def get_top_skills(self, limit: int = 10) -> List[dict]:
        """Returns the most frequent skills in job offers."""
        from sqlalchemy import func
        results = (
            self.session.query(DBSkill.name, func.count(DBSkill.id).label("count"))
            .join(DBSkill.jobs)
            .group_by(DBSkill.id)
            .order_by(func.count(DBSkill.id).desc())
            .limit(limit)
            .all()
        )
        return [{"name": r[0], "count": r[1]} for r in results]

    async def get_salary_stats(self) -> List[dict]:
        """Returns average salary stats by job type."""
        from sqlalchemy import func
        results = (
            self.session.query(
                DBJob.job_type, 
                func.avg(DBJob.salary_min).label("avg_min"),
                func.avg(DBJob.salary_max).label("avg_max")
            )
            .group_by(DBJob.job_type)
            .all()
        )
        return [
            {"job_type": r[0], "avg_min": float(r[1] or 0), "avg_max": float(r[2] or 0)} 
            for r in results
        ]

    def _to_domain(self, db_job: DBJob) -> DomainJob:
        return DomainJob(
            id=db_job.id,
            title=db_job.title,
            description=db_job.description,
            company_name=db_job.company.name,
            location=db_job.location,
            salary_min=db_job.salary_min,
            salary_max=db_job.salary_max,
            salary_currency=db_job.salary_currency,
            job_type=db_job.job_type,
            experience_level=db_job.experience_level,
            raw_url=db_job.raw_url,
            created_at=db_job.created_at
        )
