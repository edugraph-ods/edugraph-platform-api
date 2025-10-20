from typing import List, Optional
from pydantic import BaseModel

"""
CourseOut is a class that represents a course output.

Attributes:
    code (str): The code of the course.
    name (str): The name of the course.
    credits (int): The credits of the course.
    cycle (int): The cycle of the course.
    university (str): The university of the course.
    career (str): The career of the course.
    program (str): The program of the course.
    prerequisites (List[str]): The prerequisites of the course.
"""
class CourseOut(BaseModel):
    code: str
    name: str
    credits: int
    cycle: int
    university: Optional[str] = None
    career: Optional[str] = None
    program: Optional[str] = None
    prerequisites: List[str] = []

"""
CoursePlanItem is a class that represents a course plan item.

Attributes:
    code (str): The code of the course.
    name (str): The name of the course.
    credits (int): The credits of the course.
    approved (bool): The approved status of the course.
"""
class CoursePlanItem(BaseModel):
    code: str
    name: str
    credits: int
    approved: bool

"""
CyclePlan is a class that represents a cycle plan.

Attributes:
    cycle (int): The cycle of the plan.
    courses (List[CoursePlanItem]): The courses of the plan.
    total_credits (int): The total credits of the plan.
"""
class CyclePlan(BaseModel):
    cycle: int
    courses: List[CoursePlanItem]
    total_credits: int
