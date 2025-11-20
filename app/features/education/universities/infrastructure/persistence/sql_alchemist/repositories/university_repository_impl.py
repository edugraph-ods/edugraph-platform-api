from app.features.education.universities.domain.models.entities.university import University
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository
from app.features.education.universities.infrastructure.persistence.sql_alchemist.models.university_model import UniversityModel
from sqlalchemy import select, func


class UniversityRepositoryImpl(UniversityRepository):

    def __init__(self, db_session):
        self.db = db_session

    def _to_domain(self, model: UniversityModel) -> University:
        return University(
            id=model.id,
            name=model.name,
            acronym=model.acronym
        )

    async def get_all_universities(self):
        query = select(UniversityModel)
        result = await self.db.execute(query)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def find_by_name(self, name: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.name == name)

        result = await self.db.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    async def save(self, university: University) -> University:
        model = UniversityModel(
            id=university.id,
            name=university.name,
            acronym=university.acronym
        )
        self.db.add(model)
        await self.db.commit()
        return university

    async def count(self):
        result = await self.db.execute(
            select(func.count()).select_from(UniversityModel)
        )
        return result.scalar()

    async def find_by_acronym(self, acronym: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.acronym == acronym)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def find_by_id(self, id: str) -> University | None:
        query = select(UniversityModel).where(UniversityModel.id == id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

