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

        unique_items = set()
        for row in rows:
            career_name = row.get("Carrera", "").strip()
            program = row.get("Programa", "Pregrado").strip()
            university_raw = row.get("Universidad ", "").strip()
            uni_name, _ = UniversityCSVLoader.parse(university_raw)
            if career_name and uni_name:
                unique_items.add((uni_name, career_name, program))

        all_unis = await self.university_repo.get_all_universities()
        uni_by_name = {u.name: u for u in all_unis}

        existing_careers = await self.career_repo.get_all_careers()
        existing_pairs = {(c.university_id, c.name) for c in existing_careers}

        for uni_name, career_name, program in unique_items:
            university = uni_by_name.get(uni_name)
            if not university:
                print(f"[WARN] University not found: '{uni_name}' - skipping career: {career_name}")
                continue

            key = (university.id, career_name)
            if key in existing_pairs:
                continue

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
            except ValueError:
                pass