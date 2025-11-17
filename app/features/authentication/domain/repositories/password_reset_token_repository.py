from abc import ABC, abstractmethod
from typing import Sequence

from app.features.authentication.domain.models.password_reset_token import PasswordResetToken


class PasswordResetTokenRepository(ABC):
    @abstractmethod
    async def create(self, token: PasswordResetToken) -> PasswordResetToken:
        """Persist a password reset token."""
        raise NotImplementedError

    @abstractmethod
    async def find_active_by_user(self, user_id: str) -> Sequence[PasswordResetToken]:
        """Return non-expired, unused tokens for the given user."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_token_hash(self, token_hash: str) -> PasswordResetToken | None:
        """Retrieve a token by its hashed value."""
        raise NotImplementedError

    @abstractmethod
    async def mark_as_used(self, token_id: str) -> None:
        """Mark the token as used."""
        raise NotImplementedError

    @abstractmethod
    async def invalidate_tokens_for_user(self, user_id: str) -> None:
        """Invalidate existing tokens for the user (e.g., mark as used)."""
        raise NotImplementedError
