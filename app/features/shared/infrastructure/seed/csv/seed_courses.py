from app.features.education.courses.application.internal.inbound_services.use_cases.create_courses_use_case import \
    CreateCourseUseCase
from app.features.education.courses.domain.models.entities.course import Course
from app.features.education.courses.infrastructure.loaders.csv.course_csv_loader import CourseCSVLoader


class CourseSeeder:
    def __init__(self, session, course_repo, career_repo):
        self.session = session
        self.course_repo = course_repo
        self.career_repo = career_repo

    async def seed(self, path: str):
        loader = CourseCSVLoader()
        rows = loader.load(path)

        use_case = CreateCourseUseCase(self.course_repo)

        unique_rows: dict[tuple[str, str], dict] = {}
        for row in rows:
            career_name = row.get("Carrera", "").strip()
            code = row.get("codigo", "").strip()
            if not career_name or not code:
                continue
            unique_rows[(career_name, code)] = row

        careers = await self.career_repo.get_all_careers()
        career_by_name = {c.name: c for c in careers}

        existing = await self.course_repo.get_all_courses()
        existing_keys = {(c.career_id, c.code) for c in existing}

        to_create: list[Course] = []
        for (career_name, code), row in unique_rows.items():
            career = career_by_name.get(career_name)
            if not career:
                print(f"[WARN] Career not found: '{career_name}' - skipping course with code: {code}")
                continue

            key = (career.id, code)
            if key in existing_keys:
                continue

            try:
                cycle = int(row["Ciclo"]) if str(row.get("Ciclo", "")).strip() else 0
                credits = int(row["creditos"]) if str(row.get("creditos", "")).strip() else 0
            except ValueError:
                cycle = 0
                credits = 0

            name = row.get("Nombre del curso", "").strip()
            course_entity = Course.create(
                name=name,
                code=code,
                credits=credits,
                cycle=cycle,
                career_id=career.id,
            )
            to_create.append(course_entity)

        BATCH = 500
        for i in range(0, len(to_create), BATCH):
            await self.course_repo.save_many(to_create[i:i+BATCH])
