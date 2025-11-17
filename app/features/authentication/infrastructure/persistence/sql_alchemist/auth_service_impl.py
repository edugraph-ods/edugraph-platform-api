from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.features.authentication.domain.repositories.auth_service import AuthService

"""
AuthServiceImpl is an implementation of the AuthService interface.

Returns:
    AuthServiceImpl: The AuthServiceImpl instance.
"""
class AuthServiceImpl(AuthService):
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
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
    """
    create_access_token is an abstract method that creates an access token.

    Args:
        data (dict): The data to encode.

    Returns:
        str: The access token.
    """
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    """
    verify_token is an abstract method that verifies the token.

    Args:
        token (str): The token to verify.

    Returns:
        dict: The payload of the token.
    """
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return {}