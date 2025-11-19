from abc import ABC, abstractmethod

class TokenService(ABC):
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