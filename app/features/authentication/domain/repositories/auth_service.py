from abc import ABC, abstractmethod
from app.features.authentication.domain.models.user import User

class AuthService(ABC):
    """
    AuthService is an abstract base class that defines the interface for authentication services.

    Args:
        ABC (ABC): The abstract base class.

    Returns:
        AuthService: The AuthService instance.
    """
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        verify_password is an abstract method that verifies a password.

        Args:
            plain_password (str): The plain password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        pass

    @abstractmethod
    def get_password_hash(self, password: str) -> str:
        """
        get_password_hash is an abstract method that gets a password hash.

        Args:
            password (str): The password.

        Returns:
            str: The password hash.
        """
        pass

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """
        create_access_token is an abstract method that creates an access token.

        Args:
            data (dict): The data to encode.

        Returns:
            str: The access token.
        """
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """
        verify_token is an abstract method that verifies a token.

        Args:
            token (str): The token to verify.

        Returns:
            dict: The decoded token.
        """
        pass

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