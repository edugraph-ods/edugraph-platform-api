from app.features.education.courses.domain.models.entities.course_prerrequisite import CoursePrerequisite

from uuid import uuid4

from app.features.education.courses.domain.repositories.course_prerrequisite import CoursePrerequisiteRepository


class CreateCoursePrerequisiteUseCase:
    def __init__(self, repository: CoursePrerequisiteRepository):
        self.repository = repository

    async def execute(self, course_id: str, prerequisite_id: str) -> CoursePrerequisite:

        exists = await self.repository.find_by_course_and_prerequisite(course_id, prerequisite_id)
        if exists:
            return exists

        entity = CoursePrerequisite(
            id=str(uuid4()),
            course_id=course_id,
            prerequisite_id=prerequisite_id,
        )
        return await self.repository.save(entity)
