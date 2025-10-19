from typing import Dict, List, Optional
from pydantic import BaseModel
from app.api.v1.schemas.course_schema import CyclePlan


class IngestRequest(BaseModel):
    source_path: Optional[str] = None
    university: Optional[str] = None
    career: Optional[str] = None
    program: Optional[str] = None


class DetectCyclesResponse(BaseModel):
    has_cycles: bool
    cycles: List[List[str]]


class PlanRequest(BaseModel):
    max_credits: int
    approved: Optional[List[str]] = None
    target_codes: Optional[List[str]] = None
    failures: Optional[Dict[int, List[str]]] = None


class PlanResponse(BaseModel):
    total_cycles: int
    cycles: List[CyclePlan]
