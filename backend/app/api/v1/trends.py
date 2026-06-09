from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.agents.analyzer import TrendAnalysisAgent
from app.db.repositories import SQLAlchemyJobRepository

router = APIRouter()

@router.get("/", summary="Get global market trends")
async def get_market_trends(db: Session = Depends(deps.get_db)):
    """
    Returns live market trends: top skills, salary evolution, etc.
    """
    repo = SQLAlchemyJobRepository(db)
    agent = TrendAnalysisAgent(repo)
    return await agent.run()
