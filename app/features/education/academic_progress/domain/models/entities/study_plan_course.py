import uuid
from dataclasses import dataclass, field
from typing import List, Optional

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class StudyPlanCourse:
    course_id: str
    name: str
    credits: int
    status: str = "NOT_STARTED"
    prerequisites: List["StudyPlanCoursePrerequisite"] = field(default_factory=list)
    cycle_id: Optional[str] = None

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, course_id: str, name: str, credits: int, cycle_id: Optional[str] = None):
        return cls(
            course_id=course_id,
            name=name,
            credits=credits,
            cycle_id=cycle_id,
        )

    def add_prerequisite(self, prereq: "StudyPlanCoursePrerequisite"):
        self.prerequisites.append(prereq)

    def is_available(self) -> bool:
        return all(p.is_satisfied() for p in self.prerequisites)
