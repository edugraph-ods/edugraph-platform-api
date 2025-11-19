import hashlib
from typing import Dict

from app.features.authentication.users.application.internal.outbound_services.hashing_service.hashing_service import HashingService
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.authentication.users.domain.repositories.password_reset_token_repository import (
    PasswordResetTokenRepository,
)


class ConfirmPasswordResetUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: PasswordResetTokenRepository,
        hashing_service: HashingService,
    ) -> None:
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.hashing_service = hashing_service

    async def execute(self, token: str, new_password: str) -> Dict[str, object]:
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        stored_token = await self.token_repository.find_by_token_hash(token_hash)

        if stored_token is None:
            return {"success": False, "reason": "invalid_token"}

        if stored_token.used:
            return {"success": False, "reason": "token_used"}

        if stored_token.is_expired:
            return {"success": False, "reason": "token_expired"}

        user = await self.user_repository.get_user_by_id(stored_token.user_id)
        if user is None:
            return {"success": False, "reason": "user_not_found"}

        hashed_password = self.hashing_service.get_password_hash(new_password)
        await self.user_repository.update_password(user.id, hashed_password)

        await self.token_repository.invalidate_tokens_for_user(user.id)

        return {"success": True}
