from http.client import HTTPException

from app.features.education.courses.domain.repositories.course_repository import CourseRepository


from fastapi import HTTPException

class GetCourseByIdUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, course_id: str):
        print(f"[DEBUG] Buscando curso con ID: {course_id}")  # debug

        course = await self.repository.find_by_id(course_id)

        if not course:
            print(f"[DEBUG] Curso no encontrado para ID: {course_id}")  # debug
            raise HTTPException(status_code=404, detail="Course not found")

        print(f"[DEBUG] Curso encontrado: {course}")  # debug
        return course

