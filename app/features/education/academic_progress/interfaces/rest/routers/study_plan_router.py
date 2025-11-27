from fastapi import APIRouter, Depends, HTTPException

from app.features.education.academic_progress.application.internal.inbound_services.use_cases.create_study_plan_use_case import \
    CreateStudyPlanUseCase
from app.features.education.academic_progress.application.internal.inbound_services.use_cases.get_study_plan_use_case import \
    GetStudyPlanUseCase
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.repositories.study_plan_repository_impl import \
    StudyPlanRepositoryImpl
from app.features.education.academic_progress.interfaces.rest.schemas.study_plan_response import StudyPlanFullCreate
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/study-plans", tags=["Study Plans"])

def get_course_repository(db=Depends(get_db)) -> CourseRepository:
    return CourseRepositoryImpl(db)

def get_study_plan_repo(db=Depends(get_db)) -> StudyPlanRepository:
    return StudyPlanRepositoryImpl(db)

@router.post("/", status_code=201)
async def create_study_plan(
    payload: StudyPlanFullCreate,
    student_id: str,
    study_plan_repo=Depends(get_study_plan_repo),
    course_repo=Depends(get_course_repository)
):
    use_case = CreateStudyPlanUseCase(study_plan_repo, course_repo)

    try:
        plan = await use_case.execute(payload, student_id)
        return {"message": "Created", "plan": plan}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{plan_id}")
async def get_study_plan(
    plan_id: str,
    student_id: str,
    study_plan_repo=Depends(get_study_plan_repo)
):
    use_case = GetStudyPlanUseCase(study_plan_repo)

    try:
        return await use_case.execute(plan_id, student_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
