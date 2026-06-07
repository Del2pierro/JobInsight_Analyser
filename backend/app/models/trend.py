import uuid
from sqlalchemy import Column, String, Float, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class MarketTrend(Base):
    __tablename__ = "market_trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)  # skill, job_title, general
    name = Column(String, nullable=False)  # e.g., "Python", "Data Scientist"
    metric_name = Column(String, nullable=False)  # e.g., "demand", "avg_salary", "growth"
    metric_value = Column(Float, nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
