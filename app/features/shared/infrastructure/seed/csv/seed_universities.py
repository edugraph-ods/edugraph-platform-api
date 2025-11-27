from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader
from app.features.education.universities.application.internal.inbound_services.use_cases.create_university_use_case import CreateUniversityUseCase

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
            if not acronym:
                acronym = UniversityCSVLoader.generate_acronym(name)

            try:
                await use_case.execute(name=name, acronym=acronym)
            except ValueError:
                print(f"University already exists: {name}")
                pass