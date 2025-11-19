from fastapi import APIRouter, Depends, Request

from app.features.authentication.students.application.internal.inbound_services.use_cases.get_student_use_case import \
    GetStudentProfileUseCase
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.authentication.students.infrastructure.persistence.sql_alchemist.repositories.student_repository_impl import \
    StudentRepositoryImpl
from app.features.authentication.users.infrastructure.persistence.sql_alchemist.repositories.user_repository_impl import \
    UserRepositoryImpl
from app.features.authentication.students.interfaces.rest.schemas.student_profile_response import StudentProfileResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1", tags=["students"])

def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)

def get_student_repository(db=Depends(get_db)) -> StudentRepository:
    return StudentRepositoryImpl(db)

@router.get("/student/me", response_model=StudentProfileResponse, summary="Get the Student Profile")
async def get_my_student_profile(
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
):

    try:
        use_case = GetStudentProfileUseCase(student_repository, user_repository)
        result = await use_case.execute(request.state.user_id)
        return StudentProfileResponse(**result)
    except ValueError as e:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

