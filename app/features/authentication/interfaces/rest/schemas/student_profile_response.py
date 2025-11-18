from pydantic import BaseModel

class StudentProfileResponse(BaseModel):
    name: str
    email: str