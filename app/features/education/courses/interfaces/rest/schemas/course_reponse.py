from pydantic import BaseModel

class CourseResponse(BaseModel):
    id: str
    name: str
    code: str
    cycle: int
    credits: int
    prerequisite: list[str] = []

    class Config:
        from_attributes = True