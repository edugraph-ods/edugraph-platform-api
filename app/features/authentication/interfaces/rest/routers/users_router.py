import hashlib

from fastapi import APIRouter, Depends, HTTPException, status

from app.features.authentication.application.internal.outbound_services.email_service.email_service import EmailService
from app.features.authentication.domain.repositories.user_repository import UserRepository
from app.features.authentication.domain.repositories.password_reset_token_repository import PasswordResetTokenRepository
from app.features.authentication.interfaces.rest.schemas.auth_response import ProfileResponse
from app.features.authentication.interfaces.rest.schemas.password_reset_request import PasswordResetRequest
from app.features.authentication.interfaces.rest.schemas.reset_password_request import ResetPasswordRequest
from app.features.authentication.interfaces.rest.schemas.verify_recovery_code_request import (
    VerifyRecoveryCodeRequest,
)
from app.features.authentication.application.internal.inbound_services.uses_cases.password_reset_request import (
    RequestPasswordResetUseCase,
)
from app.features.authentication.application.internal.outbound_services.hashing_service.hashing_service import (
    HashingService,
)
from app.features.authentication.application.internal.outbound_services.token_service.token_service import TokenService
from app.features.authentication.infrastructure.email.gmail.services.email_service_impl import SMTPEmailService
from app.features.authentication.infrastructure.hashing.bcrypt.services.hashing_service_impl import (
    HashingServiceImpl,
)
from app.features.authentication.infrastructure.tokens.jwt.services.token_service_impl import TokenServiceImpl
from app.features.authentication.infrastructure.persistence.sql_alchemist.repositories.password_reset_token_repository_impl import (
    PasswordResetTokenRepositoryImpl,
)
from app.features.authentication.infrastructure.persistence.sql_alchemist.repositories.user_repository_impl import (
    UserRepositoryImpl,
)

from app.core.config.config import settings
from app.features.shared.infrastructure.persistence.sql_alchemist.session import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def get_user_repository(db=Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)


def get_password_reset_token_repository(
    db=Depends(get_db),
) -> PasswordResetTokenRepository:
    return PasswordResetTokenRepositoryImpl(db)


def get_email_service() -> EmailService:
    return SMTPEmailService(
        host=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        sender=settings.smtp_sender,
    )


def get_hashing_service() -> HashingService:
    return HashingServiceImpl()


def get_token_service() -> TokenService:
    return TokenServiceImpl(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        access_token_expire_minutes=settings.access_token_expire_minutes,
    )

@router.post("/recovery-code", status_code=status.HTTP_202_ACCEPTED, summary="Send a recovery code to the email service")
async def request_password_reset(
    request: PasswordResetRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: PasswordResetTokenRepository = Depends(get_password_reset_token_repository),
    email_service: EmailService = Depends(get_email_service),
) -> dict:
    use_case = RequestPasswordResetUseCase(
        user_repository=user_repository,
        token_repository=token_repository,
        email_service=email_service,
        expire_minutes=settings.password_reset_token_expire_minutes,
    )
    result = await use_case.execute(request.email)
    if not result["email_found"]:
        return {"message": "If the email exists, a reset link has been sent."}
    return {"message": "If the email exists, a reset link has been sent."}


@router.post(
    "/verify-recovery-code",
    status_code=status.HTTP_200_OK,
    summary="Verify a recovery code",
)
async def verify_recovery_code(
    request: VerifyRecoveryCodeRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: PasswordResetTokenRepository = Depends(get_password_reset_token_repository),
):
    user = await user_repository.get_user_by_email(request.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    token_hash = hashlib.sha256(request.code.encode("utf-8")).hexdigest()
    token = await token_repository.find_by_token_hash(token_hash)

    if token is None or token.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid recovery code")

    if token.used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recovery code already used")

    if token.is_expired:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Recovery code expired")

    return {"message": "Recovery code verified successfully."}


@router.put(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset user password",
)
async def reset_password(
    request: ResetPasswordRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    token_repository: PasswordResetTokenRepository = Depends(get_password_reset_token_repository),
    hashing_service: HashingService = Depends(get_hashing_service),
):
    user = await user_repository.get_user_by_email(request.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    hashed_password = hashing_service.get_password_hash(request.newPassword)
    await user_repository.update_password(user.id, hashed_password)
    await token_repository.invalidate_tokens_for_user(user.id)

    return {"message": "Password updated successfully."}
