from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.api import deps
from app.agents.analyzer import TrendAnalysisAgent
from app.agents.reporter import report_agent
from app.db.repositories import SQLAlchemyJobRepository

router = APIRouter()

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
