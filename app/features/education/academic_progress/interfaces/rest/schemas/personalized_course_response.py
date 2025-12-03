from pydantic import BaseModel

class PersonalizedCourseResponse(BaseModel):
    course_id: str
    name: str
    cycle: int
    distance: int | None
