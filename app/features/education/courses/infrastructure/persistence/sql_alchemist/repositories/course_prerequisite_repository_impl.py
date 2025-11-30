from app.features.education.courses.domain.models.entities.course_prerrequisite import CoursePrerequisite
from app.features.education.courses.domain.repositories.course_prerrequisite import CoursePrerequisiteRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.models.course_prerequisite_model import \
    CoursePrerequisiteModel
from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository
from sqlalchemy import select, func


class CoursePrerequisiteRepositoryImpl(CoursePrerequisiteRepository, BaseRepository):

    def __init__(self, db_session):
        BaseRepository.__init__(self, db_session, CoursePrerequisiteModel)
        self.session = db_session

    def _to_domain(self, model) -> CoursePrerequisite:
        return CoursePrerequisite(
            id=model.id,
            course_id=model.course_id,
            prerequisite_id=model.prerequisite_id,
        )
    async def save(self, course_prerequisite: CoursePrerequisite) -> CoursePrerequisite:
        model = CoursePrerequisiteModel(
            id=course_prerequisite.id,
            course_id=course_prerequisite.course_id,
            prerequisite_id=course_prerequisite.prerequisite_id,
        )
        await self.create(model)
        return course_prerequisite

    async def save_many(self, prereqs: list[CoursePrerequisite]) -> None:
        models = [
            CoursePrerequisiteModel(
                id=p.id,
                course_id=p.course_id,
                prerequisite_id=p.prerequisite_id,
            ) for p in prereqs
        ]
        await self.create_many(models)

    async def count(self):
        result = await self.session.execute(
            select(func.count()).select_from(CoursePrerequisiteModel)
        )
        return result.scalar()

    async def find_by_course_and_prerequisite(self, course_id: str, prerequisite_id: str) -> CoursePrerequisite | None:
        query = (
            select(CoursePrerequisiteModel)
            .where(
                CoursePrerequisiteModel.course_id == course_id,
                CoursePrerequisiteModel.prerequisite_id == prerequisite_id,
            )
            .limit(1)
        )
        result = await self.session.execute(query)
        model = result.scalars().first()
        return self._to_domain(model) if model else None

    async def find_by_course_and_prerequisite(self, course_id: str, prerequisite_id: str) -> CoursePrerequisite | None:
        query = select(CoursePrerequisiteModel).where(CoursePrerequisiteModel.course_id == course_id).where(CoursePrerequisiteModel.prerequisite_id == prerequisite_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None