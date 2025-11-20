from typing import List
from pydantic import BaseModel, Field

from app.features.education.academic_progress.interfaces.rest.schemas.course_progress_update_response import \
    CycleCourses

class AcademicProgressRequest(BaseModel):
    max_credits: int = Field(8, description="Maximum credits per cycle")
    cycles: List[CycleCourses] = Field(default_factory=list)
