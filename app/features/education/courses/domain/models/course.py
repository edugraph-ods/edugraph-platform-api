import uuid
from dataclasses import dataclass, field
from typing import List

from app.features.education.courses.domain.value_objects.course_status import CourseStatus
from app.features.education.courses.domain.value_objects.prerequisite import Prerequisites


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class Course:
    name: str
    code: str
    credits: int
    cycle: int
    career_id: str
    prerequisites: Prerequisites

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