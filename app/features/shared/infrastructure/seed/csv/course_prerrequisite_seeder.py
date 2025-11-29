from sqlalchemy import text

from app.features.education.courses.application.internal.inbound_services.use_cases.create_course_prerequisite_use_case import \
    CreateCoursePrerequisiteUseCase
from app.features.education.courses.infrastructure.loaders.csv.course_csv_loader import CourseCSVLoader
from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import UniversityCSVLoader


class CoursePrerequisiteSeeder:
    def __init__(self, session, course_repo, course_prereq_repo):
        self.session = session
        self.course_repo = course_repo
        self.course_prereq_repo = course_prereq_repo
        self.create_prereq_use_case = CreateCoursePrerequisiteUseCase(course_prereq_repo)

    async def seed(self, path: str):
        loader = CourseCSVLoader()
        rows = loader.load(path)

        result = await self.session.execute(text(
            """
            SELECT c.id, c.code, ca.name as career_name, u.name as uni_name
            FROM courses c
            JOIN careers ca ON c.career_id = ca.id
            JOIN universities u ON ca.university_id = u.id
            """
        ))

        by_uni_career_code: dict[tuple[str, str, str], str] = {}
        for cid, code, career_name, uni_raw in result.fetchall():
            uni_name, _ = UniversityCSVLoader.parse(str(uni_raw))
            by_uni_career_code[(uni_name, career_name, str(code).strip())] = str(cid)

        pairs = set()
        for row in rows:
            uni_raw = row.get("Universidad ", "").strip()
            uni_name, _ = UniversityCSVLoader.parse(uni_raw)
            career_name = row.get("Carrera", "").strip()
            course_code = row.get("codigo", "").strip()
            prerequisites_raw = row.get("Prerequisitos", "").strip()
            if not course_code or prerequisites_raw in ["-", "", "Ninguno", "NINGUNO"]:
                continue
            course_id = by_uni_career_code.get((uni_name, career_name, course_code))
            if not course_id:
                continue

            for p_code in [p.strip() for p in prerequisites_raw.split(",") if p.strip()]:
                lc = p_code.lower()
                if lc in ["ninguno", "-", "", "tbd"] or "crédit" in lc:
                    continue
                prereq_course_id = by_uni_career_code.get((uni_name, career_name, p_code))
                if not prereq_course_id or prereq_course_id == course_id:
                    continue
                pairs.add((course_id, prereq_course_id))

        for course_id, prereq_id in pairs:
            await self.create_prereq_use_case.execute(course_id, prereq_id)