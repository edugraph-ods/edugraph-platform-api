from app.features.education.universities.domain.models.entities.university import University
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository
from app.features.education.universities.infrastructure.persistence.sql_alchemist.models.university_model import UniversityModel
from sqlalchemy import select, func

from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository


class UniversityRepositoryImpl(UniversityRepository, BaseRepository):

    def __init__(self, db_session):
        BaseRepository.__init__(self, db_session, UniversityModel)
        self.session = db_session

    def _to_domain(self, model: UniversityModel) -> University:
        return University(
            id=model.id,
            name=model.name,
            acronym=model.acronym
        )

    async def get_all_universities(self):
        models = await super().get_all()
        return [self._to_domain(m) for m in models]

    async def find_by_name(self, name: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.name == name)

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, university: University) -> University:
        model = UniversityModel(
            id=university.id,
            name=university.name,
            acronym=university.acronym
        )
        await self.create(model)
        return university

    async def count(self):
        result = await self.session.execute(
            select(func.count()).select_from(UniversityModel)
        )
        return result.scalar()

    async def find_by_acronym(self, acronym: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.acronym == acronym)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def find_by_id(self, id: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.id == id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

