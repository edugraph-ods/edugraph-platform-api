from sqlalchemy import select

from app.features.authentication.students.domain.models.entities.student import Student
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.students.infrastructure.persistence.sql_alchemist.models.student_model import StudentModel
from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository


class StudentRepositoryImpl(StudentRepository, BaseRepository):
    def __init__(self, session):
        BaseRepository.__init__(self, session, StudentModel)
        self.session = session

    def _to_domain(self, model: StudentModel) -> Student:
        return Student(
            id=model.id,
            name=model.name,
            user_id=model.user_id,
            university_id=model.university_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create_student(self, user_id: str, name: str, university_id: str) -> Student:
        model = StudentModel(
            user_id=user_id,
            name=name,
            university_id=university_id,
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return self._to_domain(model)

    async def get_student_by_user_id(self, user_id: str) -> Student | None:
        result = await self.session.execute(
            select(StudentModel).where(StudentModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
