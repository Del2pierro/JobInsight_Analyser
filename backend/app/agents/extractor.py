import re
from typing import List, Dict
from app.agents.base import BaseAgent
from app.services.nlp import get_nlp_service

# ---------------------------------------------------------------------------
# Skill Taxonomy & Normalization Mapping (Domain Rule 6)
# ---------------------------------------------------------------------------
SKILL_NORMALIZATION: Dict[str, str] = {
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "py": "Python",
    "python": "Python",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "postgre": "PostgreSQL",
    "react": "React",
    "reactjs": "React",
    "next": "Next.js",
    "nextjs": "Next.js",
    "fastapi": "FastAPI",
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
}

# The list of canonical skills we want to detect
CANONICAL_SKILLS = list(set(SKILL_NORMALIZATION.values()))

class ExtractorAgent(BaseAgent):
    """
    NLP Agent responsible for extracting and normalizing tech skills.
    Uses spaCy for robust tokenization and a normalization taxonomy.
    """

    def __init__(self):
        super().__init__(name="ExtractorAgent")
        self.nlp_service = get_nlp_service()

    def run(self, text: str) -> List[str]:
        """
        Parses text, extracts skills, and normalizes them.
        Example: "Je cherche un dev JS et Postgres" -> ["JavaScript", "PostgreSQL"]
        """
        self.log_start("extract_skills", text_length=len(text))
        
        if not text:
            return []

        # Optimization: Disable heavy components for skill extraction
        doc = self.nlp_service.get_doc(text.lower(), disable_components=["parser", "ner", "lemmatizer"])
        
        extracted_skills = set()
        
        # Method 1: Token-based matching for normalization mapping
        tokens = [token.text for token in doc]
        
        # Method 2: Regex on the whole text for multi-word skills (like "Amazon Web Services")
        text_lower = text.lower()
        
        # Check for each entry in our normalization map
        for trigger, canonical in SKILL_NORMALIZATION.items():
            # Use word boundaries for safety
            pattern = r'\b' + re.escape(trigger) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.add(canonical)
                
        result = sorted(list(extracted_skills))
        self.log_end("extract_skills", skills_found=len(result))
        
        return result

# Singleton
extractor_agent = ExtractorAgent()
