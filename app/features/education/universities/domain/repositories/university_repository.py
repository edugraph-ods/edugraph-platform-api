from abc import ABC, abstractmethod

from app.features.education.universities.domain.models.university import University


class UniversityRepository(ABC):

    @abstractmethod
    async def save(self, university: University) -> University:
        pass

    @abstractmethod
    async def get_all_universities(self):
        pass

    @abstractmethod
    async def find_by_name(self, name: str):
        pass

    @abstractmethod
    async def count(self):
        pass