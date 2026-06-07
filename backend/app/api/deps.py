from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User

# OAuth2 scheme configures Swagger UI /redoc to send Bearer tokens
# The tokenUrl must match the actual login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session per request.
    Ensures the connection is always closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    FastAPI dependency that extracts the JWT token, decodes it,
    and returns the corresponding User from the database.
    Raises UnauthorizedException if the token is invalid or user doesn't exist.
    """
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Could not validate credentials or token expired")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Token missing subject claim")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException("User no longer exists")

    return user
