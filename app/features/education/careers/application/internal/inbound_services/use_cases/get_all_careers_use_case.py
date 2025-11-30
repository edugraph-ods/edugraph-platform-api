from app.features.education.careers.domain.repositories.career_repository import CareerRepository


class GetAllCareersUseCase:
    def __init__(self, repository: CareerRepository):
        self.repository = repository

    async def execute(self):
        careers = await self.repository.get_all_careers()

        if not careers:
            raise ValueError("Careers not found")

        return careers or []