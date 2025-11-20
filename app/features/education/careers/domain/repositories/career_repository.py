from abc import ABC, abstractmethod

from app.features.education.careers.domain.models.career import Career


class CareerRepository(ABC):

    @abstractmethod
    async def save(self, career: Career) -> Career:
        pass

    @abstractmethod
    async def find_by_university_and_name(self, university_id: str, name: str) -> Career | None:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Career | None:
        pass