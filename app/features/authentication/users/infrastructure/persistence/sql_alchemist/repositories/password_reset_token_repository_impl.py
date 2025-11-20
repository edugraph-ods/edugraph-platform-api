from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.authentication.users.domain.models.entities.password_reset_token import PasswordResetToken
from app.features.authentication.users.domain.repositories.password_reset_token_repository import (
    PasswordResetTokenRepository,
)
from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.password_reset_token_model import (
    PasswordResetTokenModel,
)


class PasswordResetTokenRepositoryImpl(PasswordResetTokenRepository):
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    def _to_domain(self, model: PasswordResetTokenModel) -> PasswordResetToken:
        return PasswordResetToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            used=model.used,
            created_at=model.created_at,
            updated_at=model.updated_at,
            used_at=model.used_at,
        )

    async def create(self, token: PasswordResetToken) -> PasswordResetToken:
        model = PasswordResetTokenModel(
            user_id=token.user_id,
            token_hash=token.token_hash,
            expires_at=token.expires_at,
            used=token.used,
            created_at=token.created_at,
            updated_at=token.updated_at,
            used_at=token.used_at,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return self._to_domain(model)

    async def find_active_by_user(self, user_id: int) -> Sequence[PasswordResetToken]:
        result = await self.db.execute(
            select(PasswordResetTokenModel)
            .where(
                PasswordResetTokenModel.user_id == user_id,
                PasswordResetTokenModel.used.is_(False),
                PasswordResetTokenModel.expires_at > datetime.utcnow(),
            )
            .order_by(PasswordResetTokenModel.created_at.desc())
        )
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    async def find_by_token_hash(self, token_hash: str) -> PasswordResetToken | None:
        result = await self.db.execute(
            select(PasswordResetTokenModel).where(PasswordResetTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def mark_as_used(self, token_id: int) -> None:
        await self.db.execute(
            update(PasswordResetTokenModel)
            .where(PasswordResetTokenModel.id == token_id)
            .values(
                used=True,
                used_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()

    async def invalidate_tokens_for_user(self, user_id: int) -> None:
        await self.db.execute(
            update(PasswordResetTokenModel)
            .where(
                PasswordResetTokenModel.user_id == user_id,
                PasswordResetTokenModel.used.is_(False),
            )
            .values(
                used=True,
                used_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        await self.db.commit()
