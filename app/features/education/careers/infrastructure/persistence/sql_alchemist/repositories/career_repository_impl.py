from sqlalchemy import select

from app.features.education.careers.domain.models.entities.career import Career
from app.features.education.careers.domain.repositories.career_repository import CareerRepository
from app.features.education.careers.infrastructure.persistence.sql_alchemist.models.career_model import CareerModel
from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository


class CareerRepositoryImpl(CareerRepository, BaseRepository):

    def __init__(self, db_session):
        BaseRepository.__init__(self, db_session, CareerModel)
        self.session = db_session

    def _to_domain(self, model) -> Career:
        return Career(
            id=model.id,
            name=model.name,
            program=model.program,
            university_id=model.university_id,
        )

    async def save(self, career: Career) -> Career:
        model = CareerModel(
            id=career.id,
            name=career.name,
            program=career.program,
            university_id=career.university_id,
        )
        await self.create(model)
        return career

    async def find_by_university_and_name(self, university_id: str, name: str) -> Career | None:
        query = (
            select(CareerModel)
            .where(CareerModel.university_id == university_id)
            .where(CareerModel.name == name)
        )

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        return self._to_domain(model) if model else None

    async def find_by_name(self, name: str) -> Career | None:
        query = select(CareerModel).where(CareerModel.name == name)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def find_by_university_id(self, university_id: str) -> list[Career]:
        query = select(CareerModel).where(CareerModel.university_id == university_id)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def get_all_careers(self) -> list[Career]:
        models = await super().get_all()
        return [self._to_domain(model) for model in models]