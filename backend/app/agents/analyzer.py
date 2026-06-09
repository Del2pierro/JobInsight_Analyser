from typing import Dict, List, Any
from app.agents.base import BaseAgent
from app.domain.interfaces.repositories import JobRepository

class TrendAnalysisAgent(BaseAgent):
    """
    Market Intelligence Agent.
    Transforms raw job data into high-level market indicators.
    
    Analogy: The 'Economist' who reads all the newspapers (jobs) 
    to tell you which industries are booming and which skills are in demand.
    """

    def __init__(self, job_repo: JobRepository):
        super().__init__(name="TrendAnalysisAgent")
        self.job_repo = job_repo

    async def run(self) -> Dict[str, Any]:
        """
        Computes global market trends.
        """
        self.log_start("compute_trends")
        
        # 1. Top Skills
        top_skills = await self.job_repo.get_top_skills(limit=10)
        
        # 2. Salary Analysis
        salary_stats = await self.job_repo.get_salary_stats()
        
        # 3. Market Growth (dummy indicator for now)
        # In a real app, we would compare counts over different time periods
        
        result = {
            "top_skills": top_skills,
            "salary_trends": salary_stats,
            "market_vibe": "Haussière" if len(top_skills) > 0 else "Stable"
        }
        
        self.log_end("compute_trends", skills_analyzed=len(top_skills))
        return result
