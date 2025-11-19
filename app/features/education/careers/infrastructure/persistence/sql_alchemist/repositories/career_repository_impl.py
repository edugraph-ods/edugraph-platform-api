from app.features.education.careers.domain.models.career import Career
from app.features.education.careers.domain.repositories.career_repository import CareerRepository


class CareerRepositoryImpl(CareerRepository):

    def __init__(self, db_session):
        self.db = db_session

    def _to_domain(self, model) -> Career:
        return Career(
            id=model.id,
            name=model.name,
            university_id=model.university_id,
        )

    async def save(self, career: Career) -> Career:
        model = Career(
            id=career.id,
            name=career.name,
            university_id=career.university_id,
        )
        self.db.add(model)
        await self.db.commit()
        return career

