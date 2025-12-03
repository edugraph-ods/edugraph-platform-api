from app.features.education.courses.domain.models.entities.course import Course

class AcademicGraph:
    def __init__(self, courses: list[Course]):
        self.nodes = {c.id: c for c in courses}
        self.edges = self._build_edges(courses)

    def _build_edges(self, courses: list[Course]):
        edges = []
        for course in courses:
            for prereq in course.prerequisites:
                edges.append((prereq, course.id, 1))
        return edges

    def bellman_ford(self, start: str):
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0

        for _ in range(len(self.nodes) - 1):
            updated = False
            for u, v, w in self.edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break

        for u, v, w in self.edges:
            if dist[u] + w < dist[v]:
                raise Exception("Negative cycle detected")

        return dist
