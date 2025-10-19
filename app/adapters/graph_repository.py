from typing import Iterable, List
from threading import RLock
from app.core.entities.course import Course
from app.core.ports.graph_repository import GraphRepository

"""
InMemoryGraphRepository is a class that implements the GraphRepository interface.

Attributes:
    _courses: A list of courses.
    _lock: A lock for thread safety.

Methods:
    set_courses(courses: Iterable[Course]) -> None: Sets the courses.
    get_courses() -> List[Course]: Gets the courses.
"""
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
