from pydantic import BaseModel

class CoursesResponse(BaseModel):
    id: str
    name: str
    code: str
    cycle: int
    credits: int

    class Config:
        from_attributes = True