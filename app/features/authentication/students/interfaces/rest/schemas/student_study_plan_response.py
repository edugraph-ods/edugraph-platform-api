from pydantic import BaseModel

class StudentStudyPlanResponse(BaseModel):
    plan_id: str
    name: str