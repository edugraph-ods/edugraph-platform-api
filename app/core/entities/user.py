from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

"""
User is a dataclass that represents a user.

Args:
    email (str): The user's email.
    full_name (Optional[str]): The user's full name.
    id (Optional[int]): The user's id.
    hashed_password (Optional[str]): The user's hashed password.
    is_active (bool): The user's active status.
    created_at (datetime): The user's creation date.
    updated_at (datetime): The user's update date.

Returns:
    User: The User instance.
"""
@dataclass
class User:
    email: str
    full_name: Optional[str] = None
    id: Optional[int] = None
    hashed_password: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def create(cls, email: str, full_name: Optional[str] = None) -> "User":
        """
        create is a class method that creates a new User instance.

        Args:
            email (str): The user's email.
            full_name (Optional[str]): The user's full name.

        Returns:
            User: The User instance.
        """
        return cls(
            email=email,
            full_name=full_name,
        )