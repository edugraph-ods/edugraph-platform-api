from abc import ABC, abstractmethod

class UniversityRepository(ABC):
    @abstractmethod
    async def get_all_universities(self):
        pass