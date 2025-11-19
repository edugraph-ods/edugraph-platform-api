from abc import ABC, abstractmethod

from app.features.education.careers.domain.models.career import Career


class CareerRepository(ABC):

    @abstractmethod
    async def save(self, career: Career) -> Career:
        pass