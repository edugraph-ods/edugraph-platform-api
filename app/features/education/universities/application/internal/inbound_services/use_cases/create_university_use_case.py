import uuid

from app.features.education.universities.domain.models.entities.university import University
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository


class CreateUniversityUseCase:

    def __init__(self, repository: UniversityRepository):
        self.repository = repository

    async def execute(self, name: str, acronym: str) -> University:

        existing = await self.repository.find_by_name(name)
        if existing:
            raise ValueError("University already exists")

        university = University(
            id=str(uuid.uuid4()),
            name=name,
            acronym=acronym
        )

        return await self.repository.save(university)