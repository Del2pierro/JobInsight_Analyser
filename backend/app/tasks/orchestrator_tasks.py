from app.agents.orchestrator import orchestrator_agent
from app.tasks.worker import celery_app


@celery_app.task(name="task_process_new_job", bind=True, max_retries=3)
def task_process_new_job(self, job_id: str):
    """
    Celery task that triggers the OrchestratorAgent for a new Job.
    """
    try:
        orchestrator_agent.process_new_job(job_id)
    except Exception as exc:
        # Retry exponentially if Qdrant or the DB is temporarily unavailable
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task(name="task_process_new_resume", bind=True, max_retries=3)
def task_process_new_resume(self, resume_id: str):
    """
    Celery task that triggers the OrchestratorAgent for a new Resume.
    """
    try:
        orchestrator_agent.process_new_resume(resume_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
