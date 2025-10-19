import unicodedata
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.adapters.csv_parser import CsvParser
from app.adapters.graph_repository import InMemoryGraphRepository
from app.api.v1.schemas.course_schema import CourseOut, CyclePlan
from app.api.v1.schemas.route_schema import (
    DetectCyclesResponse,
    IngestRequest,
    PlanRequest,
    PlanResponse,
)
from app.api.dependencies import get_current_active_user
from app.core.entities.user import User
from app.core.usecases.detect_cycles import DetectCyclesUseCase
from app.core.usecases.ingest_graph import IngestGraphUseCase
from app.core.usecases.plan_route import PlanRouteUseCase
from app.services.algorithm_service_impl import AlgorithmServiceImpl


router = APIRouter(prefix="/api/v1/graph", tags=["graph"])


repo = InMemoryGraphRepository()
parser = CsvParser()
algo = AlgorithmServiceImpl()


DOMAIN_UNIVERSITY_MAP = {
    "upc.edu.pe": "Universidad Peruana de Ciencias Aplicadas",
    "upn.edu.pe": "Universidad Privada del Norte",
    "utp.edu.pe": "Universidad Tecnológica del Perú",
    "unmsm.edu.pe": "Universidad Nacional Mayor de San Marcos",
}

"""
_normalize_text is a function that normalizes a text.

Args:
    value (Optional[str]): The text to normalize.

Returns:
    str: The normalized text.
"""
def _normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    norm = unicodedata.normalize("NFKD", value)
    norm = "".join(ch for ch in norm if not unicodedata.combining(ch))
    return " ".join(norm.lower().strip().split())

"""
_get_domain_filters is a function that gets the domain filters.

Args:
    user (User): The user.
    req (IngestRequest): The ingest request.

Returns:
    dict: The domain filters.
"""
def _get_domain_filters(user: User, req: IngestRequest):
    email = user.email or ""
    domain = email.split("@")[-1]
    filters = {
        "university": req.university,
        "career": req.career,
        "program": req.program,
    }
    if domain in DOMAIN_UNIVERSITY_MAP:
        filters["university"] = DOMAIN_UNIVERSITY_MAP[domain]
    return filters

"""
_filter_courses_for_domain is a function that filters the courses for the domain.

Args:
    user (User): The user.
    courses (List): The courses.

Returns:
    List: The filtered courses.
"""
def _filter_courses_for_domain(user: User, courses: List):
    email = user.email or ""
    domain = email.split("@")[-1]
    if domain in DOMAIN_UNIVERSITY_MAP:
        target_norm = _normalize_text(DOMAIN_UNIVERSITY_MAP[domain])
        filtered = []
        for c in courses:
            if c.university and target_norm in _normalize_text(c.university):
                filtered.append(c)
        return filtered
    return courses

"""
_ingest is a function that ingests the courses.

Args:
    req (IngestRequest): The ingest request.
    current_user (User): The current user.

Returns:
    List[CourseOut]: The ingested courses.
"""
@router.post("/ingest", response_model=List[CourseOut])
def ingest(req: IngestRequest, current_user: User = Depends(get_current_active_user)):
    source = req.source_path or "app/adapters/data/Malla-Curricular-Dataset.csv"
    use_case = IngestGraphUseCase(parser=parser, repository=repo)
    filters = _get_domain_filters(current_user, req)
    try:
        courses = use_case.execute(
            source_path=source,
            university=filters["university"],
            career=filters["career"],
            program=filters["program"],
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {source}")
    courses = _filter_courses_for_domain(current_user, courses)
    return [
        CourseOut(
            code=c.code,
            name=c.name,
            credits=c.credits,
            cycle=c.cycle,
            university=c.university,
            career=c.career,
            program=c.program,
            prerequisites=c.prerequisites,
        )
        for c in courses
    ]


"""
_list_courses is a function that lists the courses.

Args:
    current_user (User): The current user.

Returns:
    List[CourseOut]: The courses.
"""
@router.get("/courses", response_model=List[CourseOut])
def list_courses(current_user: User = Depends(get_current_active_user)):
    courses = _filter_courses_for_domain(current_user, repo.get_courses())
    return [
        CourseOut(
            code=c.code,
            name=c.name,
            credits=c.credits,
            cycle=c.cycle,
            university=c.university,
            career=c.career,
            program=c.program,
            prerequisites=c.prerequisites,
        )
        for c in courses
    ]


"""
_detect_cycles is a function that detects cycles.

Args:
    current_user (User): The current user.

Returns:
    DetectCyclesResponse: The cycles.
"""
@router.get("/detect-cycles", response_model=DetectCyclesResponse)
def detect_cycles(current_user: User = Depends(get_current_active_user)):
    use_case = DetectCyclesUseCase(repository=repo, algorithm=algo)
    courses = _filter_courses_for_domain(current_user, repo.get_courses())
    has_cycles, cycles = use_case.execute(courses_override=courses)
    return DetectCyclesResponse(has_cycles=has_cycles, cycles=cycles)


"""
_plan_route is a function that plans a route.

Args:
    req (PlanRequest): The plan request.
    current_user (User): The current user.

Returns:
    PlanResponse: The plan response.
"""
@router.post("/plan", response_model=PlanResponse)
def plan_route(req: PlanRequest, current_user: User = Depends(get_current_active_user)):
    approved = set(req.approved or [])
    target = set(req.target_codes or [])
    # Convert 1-based cycle numbers from API to 0-based for internal DP
    failures = {max(int(k) - 1, 0): set(v) for k, v in (req.failures or {}).items()}
    use_case = PlanRouteUseCase(repository=repo, algorithm=algo)
    courses = _filter_courses_for_domain(current_user, repo.get_courses())
    result = use_case.execute(
        max_credits=req.max_credits,
        approved=approved,
        target_codes=target,
        failures=failures,
        courses_override=courses,
    )
    return PlanResponse(
        total_cycles=result["total_cycles"],
        cycles=[
            CyclePlan(
                cycle=cyc["cycle"],
                total_credits=cyc["total_credits"],
                courses=cyc["courses"],
            )
            for cyc in result["cycles"]
        ],
    )
