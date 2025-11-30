from typing import Any, Coroutine

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.features.education.courses.domain.models.entities.course import Course
from app.features.education.courses.domain.repositories.course_repository import CourseRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.models.course_model import CourseModel
from app.features.education.courses.infrastructure.persistence.sql_alchemist.models.course_prerequisite_model import \
    CoursePrerequisiteModel
from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository


class CourseRepositoryImpl(CourseRepository, BaseRepository):

    def __init__(self, db_session):
        BaseRepository.__init__(self, db_session, CourseModel)
        self.session = db_session

    def _to_domain(self, model) -> Course:
        return Course(
            id=model.id,
            name=model.name,
            code=model.code,
            credits=model.credits,
            cycle=model.cycle,
            career_id=model.career_id,
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
        await self.create(model)
        return course

    async def save_many(self, courses: list[Course]) -> None:
        models = [
            CourseModel(
                id=c.id,
                name=c.name,
                code=c.code,
                credits=c.credits,
                cycle=c.cycle,
                career_id=c.career_id,
            ) for c in courses
        ]
        await self.create_many(models)

    async def find_by_name(self, name: str) -> Course | None:
        query = select(CourseModel).where(CourseModel.name == name)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def find_by_code(self, code: str) -> Course | None:
        query = select(CourseModel).where(CourseModel.code == code)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def find_by_career_id(self, career_id: str) -> list[Course]:
        query = (
            select(CourseModel)
            .where(CourseModel.career_id == career_id)
            .join(CourseModel.career)
            .options(
                selectinload(CourseModel.prerequisites)
                .selectinload(CoursePrerequisiteModel.prerequisite)
            )
            .order_by(CourseModel.cycle, CourseModel.code)
        )

        result = await self.session.execute(query)
        models = result.scalars().unique().all()

        courses = []
        for model in models:
            course = self._to_domain(model)
            course.prerequisites = [p.prerequisite.id for p in getattr(model, "prerequisites", []) if p.prerequisite]
            courses.append(course)

        return courses

    async def find_by_career(self, career_id: str) -> list[Course]:
        query = (
            select(CourseModel)
            .where(CourseModel.career_id == career_id)
            .join(CourseModel.career)
            .options(
                selectinload(CourseModel.prerequisites)
                .selectinload(CoursePrerequisiteModel.prerequisite)
            )
            .order_by(CourseModel.cycle, CourseModel.code)
        )

        result = await self.session.execute(query)
        models = result.scalars().unique().all()

        courses = []
        for model in models:
            course = self._to_domain(model)
            course.prerequisites = [self._to_domain(p.prerequisite) for p in getattr(model, "prerequisites", []) if
                                    p.prerequisite]
            courses.append(course)

        return courses

    async def find_by_id_with_career(self, course_id: str) -> tuple[Course, list[Any]] | None:
        result = await self.session.execute(
            select(CourseModel)
            .options(
                selectinload(CourseModel.prerequisites)
                .selectinload(CoursePrerequisiteModel.prerequisite)
            )
            .where(CourseModel.id == course_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        course = self._to_domain(model)
        prerequisites_names = [p.prerequisite.name for p in getattr(model, "prerequisites", [])]

        return course, prerequisites_names

    async def count(self):
        result = await self.session.execute(
            select(func.count()).select_from(CourseModel)
        )
        return result.scalar()

    async def get_all_courses(self) -> list[Course]:
        models = await super().get_all()
        return [self._to_domain(m) for m in models]

    async def get_by_id(self, course_id: str) -> Course | None:
        query = select(CourseModel).where(CourseModel.id == course_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

