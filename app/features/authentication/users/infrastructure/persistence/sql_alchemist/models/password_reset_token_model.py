from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String

from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.user_model import Base


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]


class PasswordResetTokenModel(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(24), primary_key=True, index=True, default=_generate_object_id)
    user_id = Column(String(24), ForeignKey("users._id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    used_at = Column(DateTime, nullable=True)
