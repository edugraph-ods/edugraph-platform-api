from abc import ABC, abstractmethod

from app.features.authentication.domain.models.student import Student


class StudentRepository(ABC):

    @abstractmethod
    async def create_student(self, user_id: str, name: str) -> Student:
        pass

    @abstractmethod
    async def get_student_by_user_id(self, user_id: str) -> Student | None:
        pass