import uuid

from app.features.education.careers.domain.models.career import Career
from app.features.education.careers.domain.repositories.career_repository import CareerRepository

class CreateCareerUseCase:

    def __init__(self, repository: CareerRepository):
        self.repository = repository

    async def execute(self, name: str, program: str, university_id: str) -> Career:

        existing = await self.repository.find_by_name(name)
        if existing:
            raise ValueError("Career already exists")

        career = Career(
            id=str(uuid.uuid4()),
            name=name,
            program=program,
            university_id=university_id
        )

        return await self.repository.save(career)