from http.client import HTTPException

from fastapi import HTTPException, status

from app.features.education.universities.domain.repositories.university_repository import UniversityRepository


class GetAllUniversitiesUseCase:
    def __init__(self, university_repository: UniversityRepository):
        self.university_repository = university_repository

    async def execute(self):
        universities = await self.university_repository.get_all_universities()

        if not universities:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No universities found"
            )

        return universities
