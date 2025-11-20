from fastapi import APIRouter, status
from fastapi.params import Depends, Path

from app.features.education.courses.application.internal.inbound_services.use_cases.get_course_by_id_use_case import \
    GetCourseByIdUseCase
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.education.courses.interfaces.rest.schemas.course_reponse import CourseResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])


def get_course_repository(db=Depends(get_db)) -> CourseRepository:
    return CourseRepositoryImpl(db)


@router.get("/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK,
            description="Get course by id")
async def get_course_by_id(
        course_id: str = Path(..., description="Course ID"),
        course_repository: CourseRepository = Depends(get_course_repository)
):
    use_case = GetCourseByIdUseCase(course_repository)
    return await use_case.execute(course_id)

