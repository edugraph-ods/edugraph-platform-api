from app.features.education.universities.domain.models.university import University
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository
from app.features.education.universities.infrastructure.persistence.sql_alchemist.models.university_model import UniversityModel


class UniversityRepositoryImpl(UniversityRepository):

    def __init__(self, db_session):
        self.db = db_session

    def _to_domain(self, model: UniversityModel) -> University:
        return University(
            id=model.id,
            name=model.name
        )

    async def get_all_universities(self):
        result = await self.db.execute(
            UniversityModel.__table__.select()
        )
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]