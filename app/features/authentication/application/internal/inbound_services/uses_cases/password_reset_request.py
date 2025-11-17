import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict

from app.features.authentication.application.internal.outbound_services.email_service.email_service import EmailService
from app.features.authentication.domain.models.password_reset_token import PasswordResetToken
from app.features.authentication.domain.repositories.auth_repository import UserRepository
from app.features.authentication.domain.repositories.password_reset_token_repository import (
    PasswordResetTokenRepository,
)


class RequestPasswordResetUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: PasswordResetTokenRepository,
        email_service: EmailService,
        expire_minutes: int,
    ) -> None:
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.email_service = email_service
        self.expire_minutes = expire_minutes

    async def execute(self, email: str) -> Dict[str, object]:
        user = await self.user_repository.get_user_by_email(email)
        if user is None:
            return {"email_found": False}

        await self.token_repository.invalidate_tokens_for_user(user.id)

        raw_token = f"{secrets.randbelow(10 ** 6):06d}"
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=self.expire_minutes)

        token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        await self.token_repository.create(token)

        await self.email_service.send_password_reset(user.email, raw_token)

        return {"email_found": True}
