from app.features.education.courses.domain.repositories.course_repository import CourseRepository


class GetAllCoursesByCareerIdUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, career_id: str):
        courses = await self.repository.find_by_career_id(career_id)

        if not courses:
            return {
                "total_courses": 0,
                "cycles": []
            }

        courses.sort(key=lambda c: c.cycle)

        grouped = {}
        for c in courses:
            grouped.setdefault(c.cycle, []).append({
                "id": c.id,
                "name": c.name,
                "code": c.code,
                "cycle": c.cycle,
                "credits": c.credits,
                "prereqs": [p.id for p in getattr(c, "prerequisites", [])],
            })

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

        return wrapper or {"total_courses": 0, "cycles": []}