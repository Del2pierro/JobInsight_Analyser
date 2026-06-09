from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Skill:
    """
    Pure Domain Entity representing a Skill.
    Zero dependencies on frameworks.
    """
    name: str
    category: str = "hard"
    id: UUID = field(default_factory=uuid4)
    canonical_name: str | None = None

    def __post_init__(self):
        if not self.canonical_name:
            self.canonical_name = self.name.lower().strip()
