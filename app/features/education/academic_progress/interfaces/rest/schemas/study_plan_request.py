from pydantic import BaseModel
from typing import List
from enum import Enum

class CourseStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PASSED = "PASSED"
    FAILED = "FAILED"

class StudyPlanCourseCreate(BaseModel):
    course_id: str
    status: CourseStatus = CourseStatus.NOT_STARTED
    prerequisites: List[str] = []

class StudyPlanCycleCreate(BaseModel):
    cycle_number: int
    courses: List[StudyPlanCourseCreate]

class StudyPlanFullCreate(BaseModel):
    name: str
    max_credits: int
    career_id: str
    cycles: List[StudyPlanCycleCreate]
