import uuid
import os
import fitz  # PyMuPDF
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.exceptions import NotFoundException
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeOut

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/me", response_model=List[ResumeOut])
def get_my_resumes(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[Resume]:
    """
    Retrieve all resumes uploaded by the currently authenticated user.
    """
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


@router.post("/upload", response_model=ResumeOut, status_code=201)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Resume:
    """
    Upload a PDF resume, extract its text, and trigger AI processing via Celery.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont supportés.")
        
    # Save the file locally
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    # Extract text using PyMuPDF
    content_text = ""
    try:
        with fitz.open(file_path) as pdf_doc:
            for page in pdf_doc:
                content_text += page.get_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de l'extraction de texte du PDF : {str(e)}")
        
    # Create DB record
    new_resume = Resume(
        id=file_id,
        user_id=current_user.id,
        content_text=content_text,
        file_path=file_path,
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    # Trigger AI processing in background
    from app.tasks.orchestrator_tasks import task_process_new_resume
    task_process_new_resume.delay(new_resume.id)
    
    return new_resume


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(
    resume_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Resume:
    """
    Get details of a specific resume.
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise NotFoundException("Resume", resume_id)
        
    return resume
