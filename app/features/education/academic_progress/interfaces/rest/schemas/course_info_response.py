from pydantic import BaseModel

class CourseInfoResponse(BaseModel):
    id: str
    name: str
    code: str