import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.exceptions import NotFoundException
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobOut, ScrapeRequest, ScrapeResponse

router = APIRouter()


@router.get("/", response_model=List[JobOut])
def list_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> List[Job]:
    """
    Retrieve a list of jobs.
    Supports pagination with skip and limit.
    """
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


@router.post("/", response_model=JobOut, status_code=201)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),  # Authentication required
) -> Job:
    """
    Create a new job entry manually.
    Requires authentication.
    """
    new_job = Job(
        id=uuid.uuid4(),
        **job_in.model_dump(),  # Pydantic v2 method
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    from app.tasks.orchestrator_tasks import task_process_new_job
    task_process_new_job.delay(new_job.id)
    
    return new_job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: str, db: Session = Depends(deps.get_db)) -> Job:
    """
    Get details of a specific job by its ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundException("Job", job_id)
    return job


# -----------------------------------------------------------------------
# Routes de Récupération d'offres Remotive
# -----------------------------------------------------------------------

@router.post("/scrape", response_model=ScrapeResponse, status_code=202)
def launch_scraping(
    request: ScrapeRequest,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Lance la récupération d'offres d'emploi en arrière-plan via Celery.

    Retourne immédiatement un task_id pour suivre la progression.
    Le frontend peut ensuite interroger GET /scrape/{task_id}/status
    pour connaître l'avancement.
    """
    from app.tasks.scraping_tasks import task_scrape_linkedin

    task = task_scrape_linkedin.delay(
        keywords=request.keywords,
        location=request.location,
        num_pages=request.num_pages,
        user_id=str(current_user.id),
    )

    return ScrapeResponse(
        task_id=task.id,
        message=f"🤖 Récupération d'offres lancée via Remotive : '{request.keywords}' ({request.num_pages} pages)",
        status="pending",
    )


@router.get("/scrape/{task_id}/status")
def get_scrape_status(task_id: str):
    """
    Vérifie l'état d'une tâche de scraping en cours.

    États possibles :
    - PENDING  : La tâche est dans la file d'attente.
    - STARTED  : Le worker a commencé le scraping.
    - SUCCESS  : Scraping terminé, les offres sont en base.
    - FAILURE  : Une erreur est survenue.
    """
    from celery.result import AsyncResult

    result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.ready():
        if result.successful():
            response["result"] = result.result
        else:
            response["error"] = str(result.result)

    return response

