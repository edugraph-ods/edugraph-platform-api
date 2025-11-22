from typing import List
from pydantic import BaseModel

from app.features.education.academic_progress.interfaces.rest.schemas.course_info_response import CourseInfoResponse


class MinPrereqPathResponse(BaseModel):
    course_id: str
    min_courses_required: int
    courses_in_order: List[CourseInfoResponse]
