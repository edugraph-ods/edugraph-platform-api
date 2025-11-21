from http.client import HTTPException

from app.features.education.courses.domain.repositories.course_repository import CourseRepository


from fastapi import HTTPException

from app.features.education.courses.interfaces.rest.schemas.course_reponse import CourseResponse


class GetCourseByIdUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, course_id: str):

        result = await self.repository.find_by_id_with_career(course_id)
        if not result:
            raise HTTPException(status_code=404, detail="Course not found")

        course, prereq_names = result

        return CourseResponse(
            id=course.id,
            name=course.name,
            code=course.code,
            cycle=course.cycle,
            credits=course.credits,
            prerequisite=prereq_names
        )

