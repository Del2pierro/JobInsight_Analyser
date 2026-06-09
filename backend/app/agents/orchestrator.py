from sqlalchemy.orm import Session

from app.agents.base import BaseAgent
from app.agents.extractor import extractor_agent
from app.agents.collector import CollectorAgent
from app.agents.analyzer import TrendAnalysisAgent
from app.agents.advisor import career_advisor_agent
from app.db.session import SessionLocal
from app.db.repositories import SQLAlchemyJobRepository
from app.models.job import Job
from app.services.embeddings import get_embedding_service
from app.services.qdrant import COLLECTION_JOBS, COLLECTION_RESUMES, get_qdrant_service


class OrchestratorAgent(BaseAgent):
    """
    The 'Conductor' of the system.
    Coordinates all specialized agents (Collector, Extractor, Matcher, Advisor).
    
    Analogy: The project manager who ensures every specialist (agents) 
    does their job in the right order to deliver the final product.
    """

    def __init__(self):
        super().__init__(name="OrchestratorAgent")
        self.embedding_service = None
        self.qdrant_service = None

    def _get_job_repo(self, db: Session) -> SQLAlchemyJobRepository:
        return SQLAlchemyJobRepository(db)

    def _ensure_services(self):
        """Lazy load services when running inside Celery."""
        if not self.embedding_service:
            self.embedding_service = get_embedding_service()
        if not self.qdrant_service:
            self.qdrant_service = get_qdrant_service()

    async def collect_and_process(self, keywords: str, location: str = "France"):
        """
        Full Pipeline: Scrape -> Save -> Extract Skills -> Vectorize.
        """
        self.log_start("collect_and_process", keywords=keywords)
        db = SessionLocal()
        repo = self._get_job_repo(db)
        
        collector = CollectorAgent(repo)
        new_jobs_count = await collector.run(keywords, location)
        
        # After collection, we could trigger analysis
        # trend_agent = TrendAnalysisAgent(repo)
        # await trend_agent.run()
        
        db.close()
        self.log_end("collect_and_process", jobs_added=new_jobs_count)
        return new_jobs_count

    def process_new_job(self, job_id: str) -> None:
        """
        Enrich a job with NLP and Vector search.
        """
        self.log_start("process_new_job", job_id=job_id)
        self._ensure_services()
        
        db = SessionLocal()
        repo = self._get_job_repo(db)
        
        try:
            job = db.query(Job).filter(Job.id == job_id).first() # Using DB model for now to get raw data
            if not job: return

            # 1. Extraction (NLP)
            skills = extractor_agent.run(job.description)
            
            # Save skills (using legacy association for now or update repo)
            # ... (skipped for brevity, but would use repositories in a full DDD impl)
            
            # 2. Vectorization (Qdrant)
            text_to_embed = f"{job.title}. {job.description} {' '.join(skills)}"
            vector = self.embedding_service.encode(text_to_embed)
            
            self.qdrant_service.upsert(
                collection=COLLECTION_JOBS,
                point_id=job.id,
                vector=vector,
                payload={
                    "title": job.title,
                    "company": job.company.name if job.company else None,
                    "skills": skills,
                    "location": job.location
                },
            )
            db.commit()
            self.log_end("process_new_job", job_id=job_id)

        except Exception as e:
            self.log_error("process_new_job", e, job_id=job_id)
        finally:
            db.close()

    async def get_career_advice(self, resume_text: str) -> str:
        """
        Get AI advice based on market context.
        """
        db = SessionLocal()
        repo = self._get_job_repo(db)
        trend_agent = TrendAnalysisAgent(repo)
        
        trends = await trend_agent.run()
        advice = await career_advisor_agent.run(resume_text, trends)
        
        db.close()
        return advice

# Singleton pattern
orchestrator_agent = OrchestratorAgent()
