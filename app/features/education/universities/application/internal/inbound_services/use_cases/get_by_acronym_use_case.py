from app.features.education.universities.domain.models.university import University
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository

class GetUniversityByAcronymUseCase:

    def __init__(self, repository: UniversityRepository):
        self.repository = repository

    async def execute(self, acronym: str) -> University:
        university = await self.repository.find_by_acronym(acronym)
        if not university:
            raise ValueError("University not found")
        return university