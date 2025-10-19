from typing import List, Optional
from pydantic import BaseModel


class CourseOut(BaseModel):
    code: str
    name: str
    credits: int
    cycle: int
    university: Optional[str] = None
    career: Optional[str] = None
    program: Optional[str] = None
    prerequisites: List[str] = []


class CoursePlanItem(BaseModel):
    code: str
    name: str
    credits: int
    approved: bool


class CyclePlan(BaseModel):
    cycle: int
    courses: List[CoursePlanItem]
    total_credits: int
