from fastapi import APIRouter

from app.features.education.academic_progress.application.internal.inbound_services.use_cases.min_prerequisite_path_use_case import \
    MinPrereqPathUseCase
from app.features.education.academic_progress.interfaces.rest.schemas.min_prerequisites_path_response import \
    MinPrereqPathResponse
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db
from fastapi import Depends

router = APIRouter(prefix="/api/v1/careers", tags=["Courses"])


def get_use_case(db=Depends(get_db)):
    repo = CourseRepositoryImpl(db)
    return MinPrereqPathUseCase(repo)


@router.get("/{career_id}/courses/{course_id}/min_prerequisites", response_model=MinPrereqPathResponse)
async def get_min_prereq(career_id: str, course_id: str, use_case: MinPrereqPathUseCase = Depends(get_use_case)):
    return await use_case.execute(career_id, course_id)
