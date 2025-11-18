from datetime import datetime, timezone
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]


"""
UserModel is a class that represents a user in the database.

Attributes:
    id: The user's ID.
    email: The user's email.
    password: The user's password.    
    recovery_code: The user's recovery code.
    recovery_code_expiration: The date and time the recovery code expires.
    is_active: Whether the user is active.
    created_at: The date and time the user was created.
    updated_at: The date and time the user was last updated.
"""
class UserModel(Base):
    __tablename__ = "users"

    id = Column("_id", String(24), primary_key=True, index=True, default=_generate_object_id)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    recovery_code = Column("recoveryCode", String(255), nullable=True)
    recovery_code_expiration = Column("recoveryCodeExpiration", DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column("createdAt", DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column("updatedAt", DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    student = relationship("StudentModel", uselist=False, back_populates="user")
