from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid

"""
User is a dataclass that represents a user.

Args:
    email (str): The user's email.
    username (str): The user's username.
    id (str): The user's identifier (24-character hex string).
    password (Optional[str]): The user's (hashed) password.
    is_active (bool): The user's active status.
    created_at (datetime): The user's creation date.
    updated_at (datetime): The user's update date.
    recovery_code (Optional[str]): The user's recovery code.
    recovery_code_expiration (Optional[datetime]): The user's recovery code expiration date.

Returns:
    User: The User instance.
"""

def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class User:
    email: str
    id: str = field(default_factory=_generate_object_id)
    password: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    recovery_code: Optional[str] = None
    recovery_code_expiration: Optional[datetime] = None

    """
    create is a class method that creates a new User instance.

    Args:
        email (str): The user's email.
        username (Optional[str]): The user's username.

    Returns:
        User: The User instance.
    """
    @classmethod
    def create(
        cls,
        email: str,
    ) -> "User":
        return cls(
            email=email,
        )