from typing import List
from pydantic import BaseModel

from app.features.education.academic_progress.domain.models.value_objects.course_status import CourseStatus

class CourseProgressUpdate(BaseModel):
    id: str
    name: str
    credits: int
    prereqs: List[str] = []
    status: CourseStatus | None = None

class CycleCourses(BaseModel):
    cycle: int
    courses: List[CourseProgressUpdate]