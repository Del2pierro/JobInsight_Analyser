from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Dict, Any
from app.domain.entities.skill import Skill

@dataclass
class Resume:
    """
    Pure Domain Entity representing a Candidate Resume.
    """
    user_id: UUID
    content_text: str
    id: UUID = field(default_factory=uuid4)
    parsed_info: Dict[str, Any] = field(default_factory=dict)
    skills: List[Skill] = field(default_factory=list)
