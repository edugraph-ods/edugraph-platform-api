from app.features.education.courses.application.internal.inbound_services.use_cases.create_courses_use_case import \
    CreateCourseUseCase
from app.features.education.courses.domain.models.course import Course
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

        for row in rows:
            cycle = int(row["Ciclo"])
            name = row["Nombre del curso"].strip()
            code = row["codigo"].strip()
            credits = int(row["creditos"])

            career_name = row.get("Carrera", "").strip()

            career = await self.career_repo.find_by_name(career_name)
            if not career:
                print(f"[WARN] Career not found: {career_name}")
                continue

            course_entity = Course.create(
                name=name,
                code=code,
                credits=credits,
                cycle=cycle,
                career_id=career.id,
            )

            try:
                await use_case.execute(
                    name=course_entity.name,
                    code=code,
                    credits=course_entity.credits,
                    cycle=course_entity.cycle,
                    career_id=course_entity.career_id
                )

            except ValueError as e:
                print(f"Error creating course '{name}': {e}")
