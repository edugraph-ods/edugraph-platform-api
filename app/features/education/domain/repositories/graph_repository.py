from abc import ABC, abstractmethod
from typing import Iterable, List
from app.features.education.domain.models.course import Course

"""
GraphRepository is an abstract base class that defines the interface for graph repositories.

Methods:
    set_courses(self, courses: Iterable[Course]) -> None:
        Sets the courses of the graph repository.
    get_courses(self) -> List[Course]:
        Gets the courses of the graph repository.
"""
class GraphRepository(ABC):
    @abstractmethod
    def set_courses(self, courses: Iterable[Course]) -> None:
        pass

    @abstractmethod
    def get_courses(self) -> List[Course]:
        pass
