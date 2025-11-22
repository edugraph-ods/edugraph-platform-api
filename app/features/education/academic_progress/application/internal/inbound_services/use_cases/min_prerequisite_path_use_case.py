from app.features.education.academic_progress.interfaces.rest.schemas.course_info_response import CourseInfoResponse
from app.features.education.academic_progress.interfaces.rest.schemas.min_prerequisites_path_response import \
    MinPrereqPathResponse
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.academic_progress.domain.models.value_objects.prerequisite import Prerequisites


class MinPrereqPathUseCase:
    def __init__(self, repository: CourseRepository):
        self.repository = repository

    async def execute(self, career_id: str, target_course_id: str):
        courses = await self.repository.find_by_career_id(career_id)
        n = len(courses)
        index_map = {c.id: i for i, c in enumerate(courses)}

        dist = [[float('inf')] * n for _ in range(n)]
        next_node = [[None] * n for _ in range(n)]

        for i, course in enumerate(courses):
            dist[i][i] = 0

            prereqs = course.prerequisites
            if isinstance(prereqs, list):
                prereqs = Prerequisites(prereqs)

            for prereq_id in prereqs.course_ids:
                if prereq_id in index_map:
                    j = index_map[prereq_id]
                    dist[j][i] = 1
                    next_node[j][i] = i

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        target_idx = index_map[target_course_id]
        min_path = []

        def reconstruct_path(start_idx, end_idx):
            path = []
            if next_node[start_idx][end_idx] is None:
                return path
            at = start_idx
            while at != end_idx:
                path.append(courses[at])
                at = next_node[at][end_idx]
            path.append(courses[end_idx])
            return path

        for i, c in enumerate(courses):
            prereqs = c.prerequisites
            if isinstance(prereqs, list):
                prereqs = Prerequisites(prereqs)

            if not prereqs.course_ids:
                path = reconstruct_path(i, target_idx)
                if path:
                    if not min_path or len(path) < len(min_path):
                        min_path = path

        return MinPrereqPathResponse(
            course_id=target_course_id,
            min_courses_required=len(min_path),
            courses_in_order=[
                CourseInfoResponse(
                    id=c.id,
                    name=c.name,
                    code=c.code
                )
                for c in min_path
            ]
        )

