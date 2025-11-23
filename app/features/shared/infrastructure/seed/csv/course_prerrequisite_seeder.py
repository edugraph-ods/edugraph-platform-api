from uuid import uuid4

from app.features.education.courses.domain.models.entities.course_prerrequisite import CoursePrerequisite
from app.features.education.courses.infrastructure.loaders.csv.course_csv_loader import CourseCSVLoader


class CoursePrerequisiteSeeder:
    def __init__(self, session, course_repo, course_prereq_repo):
        self.session = session
        self.course_repo = course_repo
        self.course_prereq_repo = course_prereq_repo

    async def seed(self, path: str):
        loader = CourseCSVLoader()
        rows = loader.load(path)

        all_courses = await self.course_repo.get_all_courses()
        by_code = {c.code.strip(): c for c in all_courses}

        pairs = set()
        for row in rows:
            course_code = row.get("codigo", "").strip()
            prerequisites_raw = row.get("Prerequisitos", "").strip()
            if not course_code or prerequisites_raw in ["-", "", "Ninguno", "NINGUNO"]:
                continue
            course = by_code.get(course_code)
            if not course:
                continue

            for p_code in [p.strip() for p in prerequisites_raw.split(",") if p.strip()]:
                lc = p_code.lower()
                if lc in ["ninguno", "-", "", "tbd"] or "crédit" in lc:
                    continue
                prereq_course = by_code.get(p_code)
                if not prereq_course or prereq_course.id == course.id:
                    continue
                pairs.add((course.id, prereq_course.id))

        entities = [
            CoursePrerequisite(
                id=str(uuid4()),
                course_id=cid,
                prerequisite_id=pid,
            ) for (cid, pid) in pairs
        ]

        BATCH = 1000
        for i in range(0, len(entities), BATCH):
            await self.course_prereq_repo.save_many(entities[i:i+BATCH])

