import uuid
from dataclasses import dataclass, field


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class CoursePrerequisite:
    course_id: str
    prerequisite_id : str

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, course_id: str, prerequisite_id: str):
        return cls(
            course_id=course_id,
            prerequisite_id=prerequisite_id,
        )
