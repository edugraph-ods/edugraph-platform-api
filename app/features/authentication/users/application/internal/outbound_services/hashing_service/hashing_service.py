from abc import ABC, abstractmethod

class HashingService(ABC):
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