from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.features.education.courses.domain.models.entities.course import Course
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.models.course_model import CourseModel


class CourseRepositoryImpl(CourseRepository):

    def __init__(self, db_session):
        self.db = db_session

    def _to_domain(self, model) -> Course:
        return Course(
            id=model.id,
            name=model.name,
            code=model.code,
            credits=model.credits,
            cycle=model.cycle,
            career_id=model.career_id,
            prerequisites=model.prerequisites,
        )

    async def save(self, course: Course) -> Course:
        model = CourseModel(
            id=course.id,
            name=course.name,
            code=course.code,
            credits=course.credits,
            cycle=course.cycle,
            career_id=course.career_id,
        )
        self.db.add(model)
        await self.db.commit()
        return course

    async def find_by_name(self, name: str) -> Course | None:
        query = select(CourseModel).where(CourseModel.name == name)

        result = await self.db.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def find_by_code(self, code: str) -> Course | None:
        query = select(CourseModel).where(CourseModel.code == code)

        result = await self.db.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def find_by_career_id(self, career_id: str) -> list[Course]:
        query = (
            select(CourseModel)
            .where(CourseModel.career_id == career_id)
            .options(selectinload(CourseModel.prerequisites))
        )

        result = await self.db.execute(query)
        models = result.scalars().all()

        courses = []
        for model in models:
            course = self._to_domain(model)
            course.prerequisites = [p.prerequisite.id for p in getattr(model, "prerequisites", [])]
            courses.append(course)

        return courses



