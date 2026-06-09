from typing import List, Dict, Any
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

@router.get("/stats", response_model=List[Dict[str, Any]])
async def get_dashboard_stats(db: Session = Depends(deps.get_db)):
    """
    Returns statistics for the dashboard KPI cards.
    """
    # This would typically call a repository method or an agent
    # Mocking real structure for frontend compatibility
    return [
        {"title": "Offres Scrappées", "value": "1,284", "change": "+12%", "description": "Offres collectées ce mois"},
        {"title": "Compétences Extraites", "value": "842", "change": "+5%", "description": "Compétences uniques identifiées"},
        {"title": "Analyses de CV", "value": "42", "change": "+18%", "description": "CV analysés par l'IA"},
        {"title": "Taux de Matching", "value": "76%", "change": "+3%", "description": "Score de compatibilité moyen"}
    ]

@router.get("/top-skills", response_model=List[Dict[str, Any]])
async def get_top_skills(db: Session = Depends(deps.get_db)):
    """
    Returns the most demanded skills for the trends chart.
    """
    repo = SQLAlchemyJobRepository(db)
    agent = TrendAnalysisAgent(repo)
    trends = await agent.run()
    return trends.get("top_skills", [])
