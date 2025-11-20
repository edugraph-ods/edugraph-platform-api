from app.features.education.careers.domain.repositories.career_repository import CareerRepository


class GetAllCareersByUniversityIdUseCase:
    def __init__(self, repository: CareerRepository):
        self.repository = repository

    async def execute(self, university_id: str):
        careers = await self.repository.find_by_university_id(university_id)

        if not careers:
            raise ValueError("Careers not found")

        return careers or []