﻿from app.features.education.courses.application.internal.inbound_services.use_cases.create_courses_use_case import \
    CreateCourseUseCase
from app.features.education.courses.domain.models.entities.course import Course
from app.features.education.courses.infrastructure.loaders.csv.course_csv_loader import CourseCSVLoader
from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader
from sqlalchemy import text

class CourseSeeder:
    def __init__(self, session, course_repo, career_repo):
        self.session = session
        self.course_repo = course_repo
        self.career_repo = career_repo

    async def seed(self, path: str):
        loader = CourseCSVLoader()
        rows = loader.load(path)

        use_case = CreateCourseUseCase(self.course_repo)

        def norm_code(value: str) -> str:
            return " ".join(value.strip().split()).upper()

        unique_rows: dict[tuple[str, str, str], dict] = {}
        for row in rows:
            university_raw = row.get("Universidad ", "").strip()
            uni_name, _ = UniversityCSVLoader.parse(university_raw)
            career_name = row.get("Carrera", "").strip()
            code = norm_code(row.get("codigo", ""))
            if not uni_name or not career_name or not code:
                continue
            unique_rows[(uni_name, career_name, code)] = row

        careers = await self.career_repo.get_all_careers()
        result = await self.session.execute(text("SELECT id, name FROM universities"))
        uni_name_by_id: dict[str, str] = {}
        for uid, raw_name in result.fetchall():
            name, _ = UniversityCSVLoader.parse(str(raw_name))
            uni_name_by_id[str(uid)] = name

        career_by_uni_and_name = {}
        for c in careers:
            uni_name = uni_name_by_id.get(c.university_id)
            if uni_name:
                career_by_uni_and_name[(uni_name, c.name)] = c

        existing = await self.course_repo.get_all_courses()
        existing_keys = {(c.career_id, norm_code(c.code)) for c in existing}

        to_create: list[Course] = []
        for (uni_name, career_name, code), row in unique_rows.items():
            career = career_by_uni_and_name.get((uni_name, career_name))
            if not career:
                print(f"[WARN] Career not found: '{uni_name}' - '{career_name}' - skipping course with code: {code}")
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