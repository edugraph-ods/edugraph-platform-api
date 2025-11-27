import uuid
from dataclasses import dataclass, field
from typing import List

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class Course:
    name: str
    code: str
    credits: int
    cycle: int
    career_id: str
    prerequisites: List[str] = field(default_factory=list)

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, name: str, code: str, credits: int, cycle: int, career_id: str):
        return cls(
            name=name,
            code=code,
            credits=credits,
            cycle=cycle,
            career_id=career_id,
        )
    def is_available(self, approved_courses: set[str]) -> bool:
        return all(prereq in approved_courses for prereq in self.prerequisites)