from typing import Iterable, List
from threading import RLock
from app.core.entities.course import Course
from app.core.ports.graph_repository import GraphRepository


class InMemoryGraphRepository(GraphRepository):
    def __init__(self):
        self._courses: List[Course] = []
        self._lock = RLock()

    def set_courses(self, courses: Iterable[Course]) -> None:
        with self._lock:
            self._courses = list(courses)

    def get_courses(self) -> List[Course]:
        with self._lock:
            return list(self._courses)
