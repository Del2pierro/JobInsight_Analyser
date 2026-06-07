from app.core.database import Base
from app.models.user import User, Report
from app.models.job import Company, Job, JobEmbedding
from app.models.skill import Skill, JobSkill
from app.models.resume import Resume, ResumeEmbedding
from app.models.match import Match
from app.models.trend import MarketTrend

__all__ = [
    "Base",
    "User",
    "Report",
    "Company",
    "Job",
    "JobEmbedding",
    "Skill",
    "JobSkill",
    "Resume",
    "ResumeEmbedding",
    "Match",
    "MarketTrend",
]