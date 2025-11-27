from fastapi import APIRouter, Depends, Request

from app.features.authentication.students.application.internal.inbound_services.use_cases.get_student_use_case import \
    GetStudentProfileUseCase
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.students.interfaces.rest.schemas.student_study_plan_response import \
    StudentStudyPlanResponse
from app.features.authentication.students.interfaces.rest.schemas.students_plans_response import \
    StudentStudyPlansResponse
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.authentication.students.infrastructure.persistence.sql_alchemist.repositories.student_repository_impl import \
    StudentRepositoryImpl
from app.features.authentication.users.infrastructure.persistence.sql_alchemist.repositories.user_repository_impl import \
    UserRepositoryImpl
from app.features.authentication.students.interfaces.rest.schemas.student_profile_response import StudentProfileResponse
from app.features.education.academic_progress.application.internal.inbound_services.use_cases.get_student_study_plan_use_case import \
    GetStudentStudyPlanUseCase
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.repositories.study_plan_repository_impl import \
    StudyPlanRepositoryImpl
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository
from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import \
    UniversityRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1", tags=["Students"])

def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)

def get_student_repository(db=Depends(get_db)) -> StudentRepository:
    return StudentRepositoryImpl(db)

def get_university_repository(db=Depends(get_db)) -> UniversityRepository:
    return UniversityRepositoryImpl(db)

def get_study_plans_repository(db=Depends(get_db)) -> StudyPlanRepository:
    return StudyPlanRepositoryImpl(db)

@router.get("/students/me", response_model=StudentProfileResponse, summary="Get the Student Profile")
async def get_my_student_profile(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
    university_repository: UniversityRepository = Depends(get_university_repository)
):

    try:
        use_case = GetStudentProfileUseCase(student_repository, user_repository, university_repository)
        result = await use_case.execute(request.state.user_id)
        return StudentProfileResponse(**result)
    except ValueError as e:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/students/{student_id}/study_plans", response_model=StudentStudyPlansResponse, summary="Get a Student Profile")
async def get_student_profile(
    student_id: str,
    study_plans_repository: StudyPlanRepository = Depends(get_study_plans_repository),
):
    use_case = GetStudentStudyPlanUseCase(study_plans_repository)
    plans = await use_case.execute(student_id)

    return StudentStudyPlansResponse(
        study_plans=[StudentStudyPlanResponse(plan_id=p.id, name=p.name) for p in plans]
    )

