from typing import Any, Dict, List, Optional
import numpy as np

from app.agents.base import BaseAgent
from app.agents.extractor import extractor_agent
from app.services.embeddings import get_embedding_service
from app.services.qdrant import COLLECTION_JOBS, get_qdrant_service


class MatcherAgent(BaseAgent):
    """
    Advanced Matching Agent.
    Combines:
    1. Semantic Similarity (Vector Search)
    2. Skill Overlap (Explicit match)
    3. Metadata Alignment (Location, Experience)
    
    Analogy: Like a specialized recruiter who doesn't just look at the 'vibe' of the CV 
    (semantics) but also checks the 'checkboxes' (skills and constraints).
    """

    def __init__(self):
        super().__init__(name="MatcherAgent")
        self.embedding_service = get_embedding_service()
        self.qdrant_service = get_qdrant_service()

    def run(
        self, 
        resume_text: str, 
        limit: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute the advanced matching process.
        Returns a list of jobs with a composite 'matching_score' (0-100).
        """
        self.log_start("advanced_match")
        
        # Step 1: Extract skills from resume for explicit overlap calculation
        resume_skills = set(extractor_agent.run(resume_text))
        
        # Step 2: Semantic search in Qdrant
        query_vector = self.embedding_service.encode(resume_text)
        search_results = self.qdrant_service.search(
            collection=COLLECTION_JOBS,
            query_vector=query_vector,
            limit=limit * 2, # Fetch more for re-ranking
            filters=filters
        )
        
        scored_results = []
        
        for hit in search_results:
            # Hit is typically a dict with 'id', 'score' (semantic), and 'payload'
            semantic_score = hit.get("score", 0.0) # Usually 0.0 to 1.0
            payload = hit.get("payload", {})
            
            # Step 3: Skill Overlap Score (normalized 0 to 1)
            job_skills = set(payload.get("skills", []))
            skill_overlap_score = 0.0
            if resume_skills and job_skills:
                common = resume_skills.intersection(job_skills)
                skill_overlap_score = len(common) / len(job_skills)
            
            # Step 4: Metadata alignment (dummy for now, can be improved)
            # Example: Location compatibility
            # location_score = 1.0 if ... else 0.5
            
            # Step 5: Composite Scoring (Domain Rule 6)
            # Weights: 50% Semantics, 40% Skills, 10% Metadata
            final_score = (
                (semantic_score * 50) + 
                (skill_overlap_score * 40) +
                (1.0 * 10) # Placeholder for metadata
            )
            
            # Ensure 0-100 range
            final_score = min(max(final_score, 0.0), 100.0)
            
            hit["matching_score"] = round(final_score, 1)
            scored_results.append(hit)
            
        # Re-sort by the new composite score
        scored_results.sort(key=lambda x: x["matching_score"], reverse=True)
        
        result = scored_results[:limit]
        self.log_end("advanced_match", top_score=result[0]["matching_score"] if result else 0)
        
        return result


# Singleton
matcher_agent = MatcherAgent()
