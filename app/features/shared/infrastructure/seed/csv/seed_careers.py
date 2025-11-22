from app.features.education.careers.application.internal.inbound_services.use_cases.create_career_use_case import \
    CreateCareerUseCase
from app.features.education.careers.domain.models.entities.career import Career
from app.features.education.careers.infrastructure.loaders.csv.career_csv_loader import CareerCSVLoader
from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader

class CareerSeeder:
    def __init__(self, session, career_repo, university_repo):
        self.session = session
        self.career_repo = career_repo
        self.university_repo = university_repo

    async def seed(self, path: str):
        loader = CareerCSVLoader()
        rows = loader.load(path)

        use_case = CreateCareerUseCase(self.career_repo)

        for row in rows:
            career_name = row["Carrera"].strip()
            program = row.get("Programa", "Pregrado").strip()
            university_raw = row["Universidad "].strip()

            print(f"[DEBUG] Processing career: '{career_name}' for program: '{program}'")

            name, acronym = UniversityCSVLoader.parse(university_raw)

            university = await self.university_repo.find_by_name(name)
            if not university:
                print(f"[WARN] University not found: '{name}' - skipping career: {career_name}")
                continue

            print(f"[DEBUG] University found: {university.name} (ID: {university.id})")

            career_entity = Career.create(
                name=career_name,
                program=program,
                university_id=university.id
            )

            try:
                await use_case.execute(
                    name=career_entity.name,
                    program=career_entity.program,
                    university_id=career_entity.university_id
                )

            except ValueError as e:
                print(f"Error creating career '{career_name}': {e}")