import uuid
from dataclasses import field, dataclass

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class StudyPlanCoursePrerequisite:
    prerequisite_course_id: str
    study_plan_course_id: str | None = None

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, required_course_id: str, course_id: str):
        return cls(
            prerequisite_course_id=required_course_id,
            study_plan_course_id=course_id
        )
