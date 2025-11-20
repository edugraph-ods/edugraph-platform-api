from pydantic import BaseModel

class AcademicProgressResponse(BaseModel):
    cycles_needed_to_graduate: int