from typing import List
from pydantic import BaseModel

from app.features.authentication.students.interfaces.rest.schemas.student_study_plan_response import \
    StudentStudyPlanResponse

class StudentStudyPlansResponse(BaseModel):
    study_plans: List[StudentStudyPlanResponse]