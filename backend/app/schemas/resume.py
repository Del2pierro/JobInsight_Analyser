from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ResumeCreate(BaseModel):
    """Schema for uploading/creating a new resume."""
    content_text: str
    file_path: Optional[str] = None


class ResumeOut(BaseModel):
    """Schema for returning resume data."""
    id: str
    user_id: str
    content_text: str
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
