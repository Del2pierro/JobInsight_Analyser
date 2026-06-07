from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema for login endpoint."""
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    """Schema for registering a new user."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = "candidate"  # Default role


class UserOut(BaseModel):
    """Schema for returning user data (hides password)."""
    id: str
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        from_attributes = True  # Allows Pydantic to read from SQLAlchemy models
