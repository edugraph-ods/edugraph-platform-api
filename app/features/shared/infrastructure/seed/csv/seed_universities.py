import asyncio

from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader
from app.features.education.universities.application.internal.inbound_services.use_cases.create_university_use_case import CreateUniversityUseCase
from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import UniversityRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import async_session_maker

async def seed():
    async with async_session_maker() as session:
        repository = UniversityRepositoryImpl(session)
        use_case = CreateUniversityUseCase(repository)

        await UniversityCSVLoader.load_and_insert(
            "data/universities.data",
            use_case
        )

if __name__ == "__main__":
    asyncio.run(seed())