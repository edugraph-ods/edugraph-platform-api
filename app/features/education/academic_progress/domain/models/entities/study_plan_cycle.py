from dataclasses import field, dataclass
from typing import List

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]
@dataclass
class StudyPlanCycle:
    cycle_number: int
    study_plan_id: str
    courses: List["StudyPlanCourse"] = field(default_factory=list)

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, cycle_number: int, study_plan_id: str):
        return cls(
            cycle_number=cycle_number,
            study_plan_id=study_plan_id,
        )

    def add_course(self, course: "StudyPlanCourse"):
        self.courses.append(course)

    def total_credits(self) -> int:
        return sum(c.credits for c in self.courses)
