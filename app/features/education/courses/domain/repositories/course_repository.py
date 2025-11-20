from abc import ABC, abstractmethod

from app.features.education.courses.domain.models.course import Course

class CourseRepository(ABC):

    @abstractmethod
    async def save(self, career: Course) -> Course:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Course | None:
        pass

    @abstractmethod
    async def find_by_code(self, code: str) -> Course | None:
        pass