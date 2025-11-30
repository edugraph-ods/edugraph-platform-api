from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.features.education.academic_progress.application.internal.inbound_services.use_cases.create_study_plan_use_case import \
    CreateStudyPlanUseCase
from app.features.education.academic_progress.application.internal.inbound_services.use_cases.delete_study_plan_use_case import \
    DeleteStudyPlanUseCase
from app.features.education.academic_progress.application.internal.inbound_services.use_cases.get_study_plan_detail_use_case import \
    GetStudyPlanDetailUseCase
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.repositories.study_plan_repository_impl import \
    StudyPlanRepositoryImpl
from app.features.education.academic_progress.interfaces.rest.schemas.study_plan_detail_response import \
    StudyPlanDetailResponse, StudyPlanCourseDetailResponse, StudyPlanCycleDetailResponse
from app.features.education.academic_progress.interfaces.rest.schemas.study_plan_request import StudyPlanFullCreate
from app.features.education.academic_progress.interfaces.rest.schemas.study_plan_message_response import StudyPlanMessageResponse
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/study-plans", tags=["Study Plans"])

def get_course_repository(db=Depends(get_db)) -> CourseRepository:
    return CourseRepositoryImpl(db)

def get_study_plan_repository(db=Depends(get_db)) -> StudyPlanRepository:
    return StudyPlanRepositoryImpl(db)


@router.post("", status_code=201, response_model=StudyPlanMessageResponse)
async def create_study_plan(
    payload: StudyPlanFullCreate,
    student_id: str = Query(..., description="Student ID"),
    study_plan_repo=Depends(get_study_plan_repository),
    course_repo=Depends(get_course_repository)
):
    use_case = CreateStudyPlanUseCase(study_plan_repo, course_repo)

    try:
        await use_case.execute(payload, student_id)
        return StudyPlanMessageResponse(
            message="Study plan created successfully"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{plan_id}", response_model=StudyPlanMessageResponse, status_code=200)
async def delete_study_plan(
    plan_id: str,
    study_plan_repo: StudyPlanRepository = Depends(get_study_plan_repository)
):
    use_case = DeleteStudyPlanUseCase(study_plan_repo)

    try:
        await use_case.execute(plan_id)
        return StudyPlanMessageResponse(message=f"Study plan {plan_id} deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/study_plans/{plan_id}", response_model=StudyPlanDetailResponse)
async def get_study_plan_detail(
    plan_id: str,
    study_plan_repo: StudyPlanRepositoryImpl = Depends(get_study_plan_repository)
):
    use_case = GetStudyPlanDetailUseCase(study_plan_repo)
    try:
        plan = await use_case.execute(plan_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    cycles = []
    for cycle_model in plan.cycles:
        courses = []
        for course_model in cycle_model.courses:
            prerequisites = [p.prerequisite_course_code for p in course_model.prerequisites]
            courses.append(StudyPlanCourseDetailResponse(
                course_id=course_model.course_id,
                name=course_model.name,
                credits=course_model.credits,
                status=course_model.status,
                prerequisites=prerequisites
            ))
        cycles.append(StudyPlanCycleDetailResponse(
            cycle_number=cycle_model.cycle_number,
            courses=courses
        ))

    return StudyPlanDetailResponse(
        plan_id=plan.id,
        name=plan.name,
        max_credits=plan.max_credits,
        career_id=plan.career_id,
        cycles=cycles
    )
