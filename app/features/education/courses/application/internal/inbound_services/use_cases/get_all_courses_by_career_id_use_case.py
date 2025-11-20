from app.features.education.courses.domain.repositories.course_repository import CourseRepository


class GetAllCoursesByCareerIdUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, university_id: str):
        courses = await self.repository.find_by_career_id(university_id)


        if not courses:
            raise ValueError("Courses not found")

        courses.sort(key=lambda c: c.cycle)

        grouped = {}
        for c in courses:
            grouped.setdefault(c.cycle, []).append(c)

        wrapper = {
            "total_courses": len(courses),
            "cycles": [
                {
                    "cycle": cycle,
                    "courses": grouped[cycle]
                }
                for cycle in sorted(grouped.keys())
            ]
        }

        return wrapper or None