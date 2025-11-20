from select import select

from app.features.education.courses.domain.models.course_prerrequisite import CoursePrerequisite
from app.features.education.courses.domain.repositories.course_prerrequisite import CoursePrerequisiteRepository
from app.features.education.courses.infrastructure.persistence.sql_alchemist.models.course_prerequisite_model import \
    CoursePrerequisiteModel


class CoursePrerequisiteRepositoryImpl(CoursePrerequisiteRepository):

    def __init__(self, db_session):
        self.db = db_session

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
        self.db.add(model)
        await self.db.commit()
        return course_prerequisite