from fastapi import APIRouter, status
from fastapi.params import Depends

from app.features.education.universities.application.internal.inbound_services.use_cases.get_all_universities_use_case import \
    GetAllUniversitiesUseCase
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository
from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import \
    UniversityRepositoryImpl
from app.features.education.universities.interfaces.rest.schemas.universities_response import UniversityResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/universities", tags=["universities"])

def get_university_repository(db=Depends(get_db)) -> UniversityRepository:
    return UniversityRepositoryImpl(db)

@router.get("", response_model=list[UniversityResponse], status_code=status.HTTP_200_OK)
async def get_universities(
    repo: UniversityRepository = Depends(get_university_repository)
):
    use_case = GetAllUniversitiesUseCase(repo)
    return await use_case.execute()