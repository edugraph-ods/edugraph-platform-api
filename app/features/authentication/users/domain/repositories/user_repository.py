from abc import ABC, abstractmethod
from app.features.authentication.users.domain.models.user import User

class UserRepository(ABC):
    """
    UserRepository is an abstract base class that defines the interface for user repositories.

    Args:
        ABC (ABC): The abstract base class.

    Returns:
        UserRepository: The UserRepository instance.
    """
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """
        get_user_by_email is an abstract method that gets a user by email.

        Args:
            email (str): The user's email.

        Returns:
            User | None: The user if found, None otherwise.
        """
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """
        create_user is an abstract method that creates a new user.

        Args:
            user (User): The user to create.

        Returns:
            User: The created user.
        """
        pass

    @abstractmethod
    async def user_exists(self, email: str) -> bool:
        """
        user_exists is an abstract method that checks if a user exists.

        Args:
            email (str): The user's email.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User | None:
        """Retrieve a user by their identifier."""
        pass

    @abstractmethod
    async def update_password(self, user_id: str, hashed_password: str) -> None:
        """Persist a new hashed password for the user."""
        pass