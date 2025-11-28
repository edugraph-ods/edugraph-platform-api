from abc import ABC, abstractmethod

from app.features.education.courses.domain.models.entities.course import Course

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

    @abstractmethod
    async def find_by_career_id(self, career_id: str) -> list[Course]:
        pass

    @abstractmethod
    async def find_by_id_with_career(self, course_id: str) -> Course | None:
        pass

    @abstractmethod
    async def get_by_id(self, course_id: str) -> Course | None:
        pass