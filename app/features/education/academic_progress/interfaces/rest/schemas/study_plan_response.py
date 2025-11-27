from pydantic import BaseModel
from typing import List

class StudyPlanCourseCreate(BaseModel):
    course_id: int
    status: str = "planned"
    prerequisites: List[int] = []

class StudyPlanCycleCreate(BaseModel):
    cycle_number: int
    courses: List[StudyPlanCourseCreate]

class StudyPlanFullCreate(BaseModel):
    name: str
    max_credits: int
    career_id: int
    cycles: List[StudyPlanCycleCreate]
