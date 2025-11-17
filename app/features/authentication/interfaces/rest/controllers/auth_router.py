from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.features.authentication.interfaces.rest.dtos.auth_schema import SignUpRequest, SignInRequest, AuthResponse
from app.features.authentication.application.internal.uses_cases.signup import SignUpUseCase
from app.features.authentication.application.internal.uses_cases.signin import SignInUseCase
from app.features.authentication.domain.repositories.auth_service import AuthService, UserRepository
from app.features.authentication.infrastructure.persistence.sql_alchemist.auth_service_impl import AuthServiceImpl
from app.features.authentication.domain.repositories.user_repository_sql import UserRepositorySQL
from app.shared.infrastructure.persistence.sql_alchemist.session import get_db

bearer_scheme = HTTPBearer(description="Enter the JWT token using the format: Bearer <token>")

router = APIRouter(prefix="/api/v1", tags=["authentication"])

"""
get_auth_service is a function that returns an AuthService instance.

Returns:
    AuthService: The AuthService instance.
"""
def get_auth_service() -> AuthService:
    return AuthServiceImpl(secret_key="your-secret-key-change-in-production")

"""
get_user_repository is a function that returns a UserRepository instance.

Args:
    db (AsyncSession): The database session.

Returns:
    UserRepository: The UserRepository instance.
"""
def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositorySQL(db)

"""
sign_up is a function that handles the sign-up process.

Args:
    request (SignUpRequest): The sign-up request.
    user_repository (UserRepository): The user repository.
    auth_service (AuthService): The authentication service.

Returns:
    UserRepository: The UserRepository instance.
"""
def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositorySQL(db)

@router.post("/sign-up", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
    request: SignUpRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        use_case = SignUpUseCase(user_repository, auth_service)
        result = await use_case.execute(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

"""
sign_in is a function that handles the sign-in process.

Args:
    request (SignInRequest): The sign-in request.
    user_repository (UserRepository): The user repository.
    auth_service (AuthService): The authentication service.

Returns:
    UserRepository: The UserRepository instance.
"""
@router.post("/sign-in", response_model=AuthResponse)
async def sign_in(
    request: SignInRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        use_case = SignInUseCase(user_repository, auth_service)
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

"""
get_current_user is a function that gets the current user.

Args:
    credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.
    auth_service (AuthService): The authentication service.
    user_repository (UserRepository): The user repository.

Returns:
    UserRepository: The UserRepository instance.
"""
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    user_repository: UserRepository = Depends(get_user_repository)
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