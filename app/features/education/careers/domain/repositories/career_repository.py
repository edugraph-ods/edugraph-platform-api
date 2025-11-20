from abc import ABC, abstractmethod

from app.features.education.careers.domain.models.entities.career import Career
from typing import List


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

    @abstractmethod
    async def find_by_university_id(self, university_id: str) -> List[Career]:
        pass

    @abstractmethod
    async def get_all_careers(self) -> List[Career]:
        pass