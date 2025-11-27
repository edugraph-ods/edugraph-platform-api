from pydantic import BaseModel
from typing import List
from enum import Enum

class CourseStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PASSED = "PASSED"
    FAILED = "FAILED"

class StudyPlanCourseDetailResponse(BaseModel):
    course_id: str
    name: str
    credits: int
    status: CourseStatus
    prerequisites: List[str] = []

class StudyPlanCycleDetailResponse(BaseModel):
    cycle_number: int
    courses: List[StudyPlanCourseDetailResponse]

class StudyPlanDetailResponse(BaseModel):
    plan_id: str
    name: str
    max_credits: int
    career_id: str
    cycles: List[StudyPlanCycleDetailResponse]
