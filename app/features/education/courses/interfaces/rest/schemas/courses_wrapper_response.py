from pydantic import BaseModel
from typing import List

from app.features.education.courses.interfaces.rest.schemas.cycle_group_response import CycleGroup

class CoursesWrapperResponse(BaseModel):
    total_courses: int
    cycles: List[CycleGroup]