from abc import ABC, abstractmethod
from typing import Iterable, Optional
from app.core.entities.course import Course


class Parser(ABC):
    @abstractmethod
    def load_courses(
        self,
        source_path: str,
        university: Optional[str] = None,
        career: Optional[str] = None,
        program: Optional[str] = None,
    ) -> Iterable[Course]:
        pass
