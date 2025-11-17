from passlib.context import CryptContext

from app.features.authentication.application.internal.outbound_services.hashing_service.hashing_service import HashingService


"""    
HashingService is an implementation of the HashingService interface.
"""
class HashingServiceImpl(HashingService):
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            deprecated="auto",
        )

    """
    verify_password is an abstract method that verifies the password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    """
    get_password_hash is an abstract method that gets the password hash.

    Args:
        password (str): The password.

    Returns:
        str: The password hash.
    """
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)