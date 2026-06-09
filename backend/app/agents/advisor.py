from typing import Dict, List, Any
from app.agents.base import BaseAgent
from app.services.llm import get_gemini_service
from app.agents.matcher import matcher_agent

class CareerAdvisorAgent(BaseAgent):
    """
    AI Career Advisor Agent (RAG).
    Provides personalized advice based on market data and candidate profile.
    
    Analogy: The 'Mentor' who knows the market inside out and helps you 
    navigate your career path with wisdom and data.
    """

    def __init__(self):
        super().__init__(name="CareerAdvisorAgent")
        self.llm_service = get_gemini_service()

    async def run(self, resume_text: str, market_trends: Dict[str, Any]) -> str:
        """
        Generates personalized career advice using RAG.
        """
        self.log_start("generate_career_advice")
        
        # 1. Retrieval: Get matching jobs for context
        matches = matcher_agent.run(resume_text, limit=3)
        
        # 2. Augmentation: Prepare the prompt with context
        context_jobs = "\n".join([
            f"- {m['payload'].get('title')} chez {m['payload'].get('company')} ({m['matching_score']}%)"
            for m in matches
        ])
        
        top_skills = ", ".join([s['name'] for s in market_trends.get("top_skills", [])[:5]])
        
        prompt = f"""
        Tu es un expert en recrutement et conseiller de carrière pour JobInsight AI.
        
        Voici le contexte du candidat :
        - Compétences actuelles extraites de son CV : {resume_text[:500]}...
        
        Contexte du marché actuel :
        - Compétences les plus demandées : {top_skills}
        - Tendance générale : {market_trends.get('market_vibe')}
        
        Meilleures opportunités trouvées pour lui :
        {context_jobs}
        
        Donne-lui 3 conseils concrets pour booster sa carrière ce mois-ci. 
        Sois encourageant, professionnel et précis. Utilise les données fournies.
        Réponds en français.
        """
        
        # 3. Generation
        advice = await self.llm_service.generate_advice(prompt)
        
        self.log_end("generate_career_advice")
        return advice

# Singleton
career_advisor_agent = CareerAdvisorAgent()
