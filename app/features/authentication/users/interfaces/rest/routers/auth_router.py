from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.features.authentication.users.application.internal.outbound_services.hashing_service.hashing_service import \
    HashingService
from app.features.authentication.users.application.internal.outbound_services.token_service.token_service import TokenService
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.interfaces.rest.schemas.auth_response import AuthResponse

from app.features.authentication.users.interfaces.rest.schemas.sign_up_request import SignUpRequest
from app.features.authentication.users.interfaces.rest.schemas.sign_in_request import SignInRequest
from app.features.authentication.users.application.internal.inbound_services.uses_cases.sign_up_use_case import SignUpUseCase
from app.features.authentication.users.application.internal.inbound_services.uses_cases.sign_in_use_case import SignInUseCase
from app.features.authentication.users.infrastructure.hashing.bcrypt.services.hashing_service_impl import HashingServiceImpl
from app.features.authentication.users.infrastructure.tokens.jwt.services.token_service_impl import TokenServiceImpl
from app.features.authentication.users.infrastructure.persistence.sql_alchemist.repositories.user_repository_impl import UserRepositoryImpl
from app.features.authentication.students.infrastructure.persistence.sql_alchemist.repositories.student_repository_impl import StudentRepositoryImpl

from app.core.config.config import settings
from app.features.shared.infrastructure.persistence.sql_alchemist.session import get_db

bearer_scheme = HTTPBearer(description="Enter the JWT token using the format: Bearer <token>")

router = APIRouter(prefix="/api/v1", tags=["authentication"])


def get_auth_service() -> HashingService:
    return HashingServiceImpl()


def get_jwt_service() -> TokenService:
    return TokenServiceImpl(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)


def get_student_repository(db=Depends(get_db)) -> StudentRepository:
    return StudentRepositoryImpl(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: TokenService = Depends(get_jwt_service),
    user_repository: UserRepository = Depends(get_user_repository),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = auth_service.verify_token(credentials.credentials)
    if not payload:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = await user_repository.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


@router.post("/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(
    request: SignUpRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
    hash_service: HashingService = Depends(get_auth_service),
):
    try:
        use_case = SignUpUseCase(user_repository, student_repository, hash_service)
        result = await use_case.execute(
            email=request.email,
            password=request.password,
            name=request.name
        )
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(
    request: SignInRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
    hash_service: HashingService = Depends(get_auth_service),
    token_service: TokenService = Depends(get_jwt_service)
):
    try:
        use_case = SignInUseCase(user_repository, student_repository, hash_service, token_service)
        result = await use_case.execute(
            email=request.email,
            password=request.password
        )
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )