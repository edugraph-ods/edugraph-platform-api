from pydantic import BaseModel

class StudentProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    university: str
    university_id: str