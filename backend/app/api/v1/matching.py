from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.agents.matcher import matcher_agent
from app.core.exceptions import NotFoundException
from app.models.resume import Resume
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.post("/resume/{resume_id}", response_model=List[Dict[str, Any]])
def match_resume_to_jobs(
    resume_id: str,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Dict[str, Any]]:
    """
    Match a user's resume against all jobs in Qdrant using semantic vector search.
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise NotFoundException("Resume", resume_id)

    # Search similar jobs in Qdrant
    matches = matcher_agent.run(resume_text=resume.content_text, limit=limit)
    return matches


@router.post("/job/{job_id}", response_model=Dict[str, Any])
def match_job_to_resumes(
    job_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Dict[str, Any]:
    """
    Calculate compatibility score of a job against all user's resumes.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundException("Job", job_id)

    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    if not resumes:
        return {"job_id": job_id, "best_match": None, "scores": []}

    from app.services.embeddings import get_embedding_service
    from app.services.qdrant import get_qdrant_service, COLLECTION_JOBS
    
    embedding_service = get_embedding_service()
    qdrant_service = get_qdrant_service()

    # Search for this specific job in Qdrant to get its vector representation
    # (Or construct it from database fields)
    from qdrant_client.http import models as qmodels
    try:
        points = qdrant_service._client.retrieve(
            collection_name=COLLECTION_JOBS,
            ids=[job_id],
            with_vectors=True
        )
        if not points:
            # Fallback: create vector representation on the fly
            skills_list = [s.skill.name for s in job.skills]
            text = f"{job.title}. {job.description} {' '.join(skills_list)}"
            job_vector = embedding_service.encode(text)
        else:
            job_vector = points[0].vector
    except Exception:
        # Fallback
        skills_list = [s.skill.name for s in job.skills]
        text = f"{job.title}. {job.description} {' '.join(skills_list)}"
        job_vector = embedding_service.encode(text)

    scores = []
    import numpy as np

    for resume in resumes:
        resume_vector = embedding_service.encode(resume.content_text)
        # Cosine similarity
        dot_product = np.dot(job_vector, resume_vector)
        norm_a = np.linalg.norm(job_vector)
        norm_b = np.linalg.norm(resume_vector)
        score = float(dot_product / (norm_a * norm_b)) if norm_a and norm_b else 0.0
        
        scores.append({
            "resume_id": str(resume.id),
            "resume_filename": resume.file_path.split("_")[-1] if resume.file_path else "CV",
            "score": round(score, 4)
        })

    scores.sort(key=lambda x: x["score"], reverse=True)

    return {
        "job_id": job_id,
        "best_match": scores[0] if scores else None,
        "scores": scores
    }

@router.get("/resume-analysis", response_model=Dict[str, Any])
def get_resume_analysis_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Dict[str, Any]:
    """
    Get a comprehensive analysis summary of the user's best resume.
    """
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found for this user")

    # This would involve calling the CVMatchingAgent and CareerAdvisorAgent
    # For now, providing the structure expected by the frontend
    # In a real scenario, this would be computed by the agents
    return {
        "score": 84,
        "top_matches": [
            {"id": "1", "title": "Senior React Developer", "company": "TechFlow", "match_score": 92},
            {"id": "2", "title": "Fullstack Engineer (Node/React)", "company": "CloudScale", "match_score": 88},
            {"id": "3", "title": "Frontend Architect", "company": "Creative Studio", "match_score": 79},
        ],
        "recommendations": [
            "Ajoutez des projets concrets utilisant Docker pour renforcer votre profil DevOps.",
            "Certifiez vos compétences en TypeScript pour accéder à des postes de Lead.",
            "Mettez en avant votre expérience en gestion d'équipe."
        ],
        "missing_skills": ["Docker", "Kubernetes", "GraphQL", "Unit Testing"],
        "strengths": ["React", "Next.js", "Tailwind CSS", "Architecture Logicielle"]
    }
