from typing import Dict, List, Optional
from pydantic import BaseModel
from app.api.v1.schemas.course_schema import CyclePlan

"""
IngestRequest is a class that represents an ingest request.

Attributes:
    source_path (Optional[str]): The source path of the ingest request.
    university (Optional[str]): The university of the ingest request.
    career (Optional[str]): The career of the ingest request.
    program (Optional[str]): The program of the ingest request.
"""
class IngestRequest(BaseModel):
    source_path: Optional[str] = None
    university: Optional[str] = None
    career: Optional[str] = None
    program: Optional[str] = None

"""
DetectCyclesResponse is a class that represents a detect cycles response.

Attributes:
    has_cycles (bool): The has cycles of the detect cycles response.
    cycles (List[List[str]]): The cycles of the detect cycles response.
"""
class DetectCyclesResponse(BaseModel):
    has_cycles: bool
    cycles: List[List[str]]

"""
PlanRequest is a class that represents a plan request.

Attributes:
    max_credits (int): The max credits of the plan request.
    approved (Optional[List[str]]): The approved of the plan request.
    target_codes (Optional[List[str]]): The target codes of the plan request.
    failures (Optional[Dict[int, List[str]]]): The failures of the plan request.
"""
class PlanRequest(BaseModel):
    max_credits: int
    approved: Optional[List[str]] = None
    target_codes: Optional[List[str]] = None
    failures: Optional[Dict[int, List[str]]] = None

"""
PlanResponse is a class that represents a plan response.

Attributes:
    total_cycles (int): The total cycles of the plan response.
    cycles (List[CyclePlan]): The cycles of the plan response.
"""
class PlanResponse(BaseModel):
    total_cycles: int
    cycles: List[CyclePlan]
