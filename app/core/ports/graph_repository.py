from abc import ABC, abstractmethod
from typing import Iterable, List
from app.core.entities.course import Course


class GraphRepository(ABC):
    @abstractmethod
    def set_courses(self, courses: Iterable[Course]) -> None:
        pass

    @abstractmethod
    def get_courses(self) -> List[Course]:
        pass
