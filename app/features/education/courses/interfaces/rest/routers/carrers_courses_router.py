from fastapi import APIRouter, status
from fastapi.params import Depends, Path

from app.features.education.careers.application.internal.inbound_services.use_cases.get_all_careers_by_university_id_use_case import \
    GetAllCareersByUniversityIdUseCase
from app.features.education.careers.domain.repositories.career_repository import CareerRepository
from app.features.education.careers.infrastructure.persistence.sql_alchemist.repositories.career_repository_impl import \
    CareerRepositoryImpl
from app.features.education.careers.interfaces.rest.schemas.careers_response import CareersResponse
from app.features.education.courses.application.internal.inbound_services.use_cases.get_all_courses_by_career_id_use_case import \
    GetAllCoursesByCareerIdUseCase
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.education.courses.interfaces.rest.schemas.courses_response import CoursesResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/careers", tags=["Careers"])

def get_course_repository(db=Depends(get_db)) -> CourseRepository:
    return CourseRepositoryImpl(db)

@router.get("/{career_id}/courses", response_model=list[CoursesResponse], status_code=status.HTTP_200_OK, description="Get all courses by career id")
async def get_courses_by_career_id(
        career_id: str = Path(..., description="Career ID"),
        course_repository: CourseRepository = Depends(get_course_repository)
):
    use_case = GetAllCoursesByCareerIdUseCase(course_repository)
    return await use_case.execute(career_id)