from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.api import deps
from app.agents.analyzer import TrendAnalysisAgent
from app.agents.reporter import report_agent
from app.db.repositories import SQLAlchemyJobRepository

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
async def list_reports(
    db: Session = Depends(deps.get_db),
    # current_user: User = Depends(deps.get_current_user),
):
    """
    List all generated reports for the user.
    """
    # In a real app, this would query a 'reports' table
    return [
        { 
            "id": "1", 
            "title": "Analyse Marché - Juin 2026", 
            "type": "market_analysis", 
            "status": "ready", 
            "created_at": "2026-06-08T10:00:00Z",
            "url": "/api/v1/reports/market-summary" 
        }
    ]

@router.get("/market-summary", summary="Download Market Report PDF")
async def download_market_report(db: Session = Depends(deps.get_db)):
    """
    Generates and returns a PDF market report.
    """
    repo = SQLAlchemyJobRepository(db)
    trend_agent = TrendAnalysisAgent(repo)
    trends = await trend_agent.run()
    
    pdf_buffer = report_agent.generate_market_report(trends)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=market_report.pdf"}
    )
