from pydantic import BaseModel

class UniversityResponse(BaseModel):
    id: str
    name: str
    acronym: str

    class Config:
        from_attributes = True