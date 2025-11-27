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

        print("\n===== STARTING PREREQUISITE SEEDER =====\n")

        total_rows = len(rows)
        print(f"Total rows read from CSV: {total_rows}\n")

        for idx, row in enumerate(rows, start=1):
            print(f"\n--- Processing row {idx}/{total_rows} ---")

            course_code = row["Codigo"].strip()
            prerequisites_raw = row["Prerequisitos"].strip()

            print(f"Current course: {course_code}")
            print(f"Raw prerequisites: '{prerequisites_raw}'")

            course = await self.course_repo.find_by_code(course_code)
            if not course:
                print(f"Course NOT found in DB: {course_code}")
                continue
            else:
                print(f"Course found in DB: {course.code} → {course.name}")

            if prerequisites_raw in ["-", "", "Ninguno", "NINGUNO"]:
                print(f"Course has no prerequisites. Skipping…")
                continue

            prereq_codes = [p.strip() for p in prerequisites_raw.split(",")]

            print(f"[INFO] Processed prerequisites list: {prereq_codes}")

            for p_code in prereq_codes:

                if p_code.lower() in ["ninguno", "-", "", "tbd"]:
                    print(f"Ignored requirement (not a course): {p_code}")
                    continue

                if "crédit" in p_code.lower():
                    print(f"Administrative requirement ignored: {p_code}")
                    continue

                print(f"Searching for prerequisite: {p_code}")

                prereq_course = await self.course_repo.find_by_code(p_code)

                if not prereq_course:
                    print(f"Prerequisite NOT found in DB: {p_code}")
                    continue
                else:
                    print(f"Prerequisite found: {prereq_course.code} → {prereq_course.name}")

                prereq_entity = CoursePrerequisite(
                    id=str(uuid4()),
                    course_id=course.id,
                    prerequisite_id=prereq_course.id,
                )

                await self.course_prereq_repo.save(prereq_entity)

                print(f"Prerequisite registered: {course.code} ← {prereq_course.code}")

