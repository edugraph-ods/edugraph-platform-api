import uuid
from dataclasses import dataclass, field
from typing import List

from app.features.education.academic_progress.domain.models.entities.study_plan_cycle import StudyPlanCycle

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]
@dataclass
class StudyPlan:
    name: str
    max_credits: int
    student_id: str
    career_id: str
    cycles: List["StudyPlanCycle"] = field(default_factory=list)

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, name: str, max_credits: int, student_id: str, career_id: str):
        return cls(
            name=name,
            max_credits=max_credits,
            student_id=student_id,
            career_id=career_id
        )

    def add_cycle(self, cycle: "StudyPlanCycle"):
        self.cycles.append(cycle)

    def total_credits(self) -> int:
        return sum(c.total_credits() for c in self.cycles)