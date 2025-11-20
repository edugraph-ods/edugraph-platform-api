from pydantic import BaseModel
class CareersResponse(BaseModel):
    id: str
    name: str
    program: str

    class Config:
        from_attributes = True