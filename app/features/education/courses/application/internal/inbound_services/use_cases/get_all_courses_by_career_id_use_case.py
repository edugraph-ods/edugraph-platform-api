from app.features.education.careers.domain.repositories.career_repository import CareerRepository
from app.features.education.courses.domain.repositories.course_repository import CourseRepository


class GetAllCoursesByCareerIdUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, university_id: str):
        courses = await self.repository.find_by_career_id(university_id)

        courses.sort(key=lambda c: c.cycle)

        if not courses:
            raise ValueError("Courses not found")

        return courses or []