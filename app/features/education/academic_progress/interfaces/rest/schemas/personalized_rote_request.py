from pydantic import BaseModel
from typing import List

class PersonalizedRouteRequest(BaseModel):
    approved_courses: List[str]
