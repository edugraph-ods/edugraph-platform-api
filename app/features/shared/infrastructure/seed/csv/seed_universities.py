import asyncio

from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader
from app.features.education.universities.application.internal.inbound_services.use_cases.create_university_use_case import CreateUniversityUseCase
from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import UniversityRepositoryImpl
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import async_session_maker

class UniversitySeeder:
    def __init__(self, session, university_repo):
        self.session = session
        self.university_repo = university_repo

    async def seed(self, path: str):
        loader = UniversityCSVLoader()
        rows = loader.load(path)

        use_case = CreateUniversityUseCase(self.university_repo)

        raw_unis = {row["Universidad "].strip() for row in rows}

        for raw in raw_unis:
            name, acronym = UniversityCSVLoader.parse(raw)

            try:
                await use_case.execute(name=name, acronym=acronym)
            except ValueError:
                # Universidad ya existe → ignorar
                pass

        print(">>> Universities seeded successfully.")