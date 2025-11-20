from pydantic import BaseModel

class AcademicProgressResponse(BaseModel):
    cycles_needed_to_graduate: int
    months_needed_to_graduate: int
    years_needed_to_graduate: float