from sqlalchemy import select

from app.features.authentication.domain.models.student import Student
from app.features.authentication.domain.repositories.student_repository import StudentRepository
from app.features.authentication.infrastructure.persistence.sql_alchemist.models.student_model import StudentModel


class StudentRepositoryImpl(StudentRepository):
    def __init__(self, db_session):
        self.db = db_session

    def _to_domain(self, model: StudentModel) -> Student:
        return Student(
            id=model.id,
            name=model.name,
            user_id=model.user_id,
            university_id=model.university_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create_student(self, user_id: str, name: str) -> Student:
        model = StudentModel(
            user_id=user_id,
            name=name,
            university_id=None,
        )

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return self._to_domain(model)

    async def get_student_by_user_id(self, user_id: str) -> Student | None:
        result = await self.db.execute(
            select(StudentModel).where(StudentModel.user_id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
