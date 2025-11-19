from app.features.education.courses.domain.models.course import Course
from app.features.education.courses.domain.repositories.course_repository import CourseRepository


class CreateCourseUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, name: str,
                      code: str,
                      credits: int,
                      cycle: int,
                      career_id: str):
        existing = await self.repository.find_by_name(name)
        if existing:
            raise ValueError("Course already exists")

        course = Course.create(
            name=name,
            code=code,
            credits=credits,
            cycle=cycle,
            career_id=career_id
        )

        return await self.repository.save(course)
