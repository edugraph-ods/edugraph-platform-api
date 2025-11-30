from typing import List

from pydantic import BaseModel

class CoursesResponse(BaseModel):
    id: str
    name: str
    code: str
    cycle: int
    credits: int
    prereqs: List[str] = []

    class Config:
        from_attributes = True