from typing import List

from pydantic import BaseModel

from app.features.education.courses.interfaces.rest.schemas.courses_response import CoursesResponse


class CycleGroup(BaseModel):
    cycle: int
    courses: List[CoursesResponse]