from fastapi import APIRouter, status
from fastapi.params import Depends, Path

from app.features.education.careers.application.internal.inbound_services.use_cases.get_all_careers_by_university_id_use_case import \
    GetAllCareersByUniversityIdUseCase
from app.features.education.careers.application.internal.inbound_services.use_cases.get_all_careers_use_case import \
    GetAllCareersUseCase
from app.features.education.careers.domain.repositories.career_repository import CareerRepository
from app.features.education.careers.infrastructure.persistence.sql_alchemist.repositories.career_repository_impl import \
    CareerRepositoryImpl
from app.features.education.careers.interfaces.rest.schemas.careers_response import CareersResponse
from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import get_db

router = APIRouter(prefix="/api/v1/careers", tags=["Careers"])

def get_career_repository(db=Depends(get_db)) -> CareerRepository:
    return CareerRepositoryImpl(db)

@router.get("", response_model=list[CareersResponse], status_code=status.HTTP_200_OK, description="Get all careers")
async def get_all_careers(
        career_repository: CareerRepository = Depends(get_career_repository)
):
    use_case = GetAllCareersUseCase(career_repository)
    return await use_case.execute()