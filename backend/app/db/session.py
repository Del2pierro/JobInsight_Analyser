from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Check connection validity before using it
    pool_size=10,        # Number of connections to keep in the pool
    max_overflow=20      # Max additional connections to allow
)

# Create SessionLocal class, which will be used to create session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
