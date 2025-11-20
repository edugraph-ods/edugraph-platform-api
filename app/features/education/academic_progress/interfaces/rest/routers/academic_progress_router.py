from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.features.education.academic_progress.application.internal.inbound_services.use_cases.academic_progress_use_case import \
    AcademicProgressUseCase
from app.features.education.academic_progress.interfaces.rest.schemas.academic_progress_requets import \
    AcademicProgressRequest
from app.features.education.courses.application.internal.inbound_services.use_cases.get_all_courses_by_career_id_use_case import \
    GetAllCoursesByCareerIdUseCase
from app.features.education.academic_progress.domain.models.entities.academic_progress import CourseProgress
from app.features.education.courses.domain.models.entities.course import Course
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.academic_progress.domain.models.value_objects.course_status import CourseStatus
from app.features.education.academic_progress.domain.models.value_objects.prerequisite import Prerequisites
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl
from app.features.education.academic_progress.interfaces.rest.schemas.academic_progress_response import AcademicProgressResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/careers", tags=["Careers"])


def get_course_repository(db=Depends(get_db)) -> CourseRepository:
    return CourseRepositoryImpl(db)

@router.post("/{career_id}/progress", response_model=AcademicProgressResponse)
async def calculate_academic_progress(
        career_id: str,
        request: AcademicProgressRequest,
        repository: CourseRepository = Depends(get_course_repository)
):
    use_case = GetAllCoursesByCareerIdUseCase(repository)
    courses_response = await use_case.execute(career_id)

    def parse_courses_from_cycles(cycles, career_id):
        courses_progress_list = []
        for cycle in cycles:
            for c in cycle.courses:
                course_obj = Course(
                    id=c.id,
                    name=c.name,
                    credits=c.credits,
                    code=c.name[:4].upper(),
                    cycle=cycle.cycle,
                    career_id=career_id,
                    prerequisites=Prerequisites(c.prereqs)
                )
                status_str = c.status.value if c.status else "NOT_STARTED"
                courses_progress_list.append(
                    CourseProgress(course=course_obj, current_cycle=cycle.cycle, status=CourseStatus(status_str))
                )
        return courses_progress_list

    courses_progress_list = parse_courses_from_cycles(request.cycles, career_id)

    service = AcademicProgressUseCase(courses_progress_list, request.max_credits)
    min_cycles = service.compute_min_cycles()

    if min_cycles is None:
        raise HTTPException(status_code=400, detail="Impossible to graduate with current course states.")

    service.update_course_availability()

    months_per_cycle = 4
    total_months = min_cycles * months_per_cycle
    years = round(total_months / 12, 2)

    return AcademicProgressResponse(
        cycles_needed_to_graduate=min_cycles,
        months_needed_to_graduate=total_months,
        years_needed_to_graduate=years,
    )
