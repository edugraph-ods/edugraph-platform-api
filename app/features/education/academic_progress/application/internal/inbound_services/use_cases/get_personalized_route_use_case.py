from math import inf
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.academic_progress.domain.models.entities.AcademicGraph import AcademicGraph

class GetPersonalizedRouteUseCase:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    async def execute(self, career_id: str, approved: list[str]):
        courses = await self.course_repository.find_by_career(career_id)
        graph = AcademicGraph(courses)

        distances = {c.id: inf for c in courses}
        for c in approved:
            distances[c] = 0

        for k, v in distances.items():
            print(k, v)

        changed = True
        while changed:
            changed = False
            for course in courses:
                if not course.prerequisites:
                    continue
                max_prereq_distance = max(
                    (distances.get(p.id if hasattr(p, "id") else p, inf) for p in course.prerequisites),
                    default=inf
                )
                new_distance = max_prereq_distance + 1 if max_prereq_distance != inf else inf
                if new_distance < distances[course.id]:
                    distances[course.id] = new_distance
                    changed = True

        result = []
        for course in courses:
            d = distances[course.id]
            if d == inf:
                d = None
            result.append({
                "course_id": course.id,
                "name": course.name,
                "cycle": course.cycle,
                "distance": d
            })

        result.sort(key=lambda x: (x["distance"] if x["distance"] is not None else inf))
        return result
