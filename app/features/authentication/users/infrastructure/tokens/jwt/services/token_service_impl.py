from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.features.authentication.users.application.internal.outbound_services.token_service.token_service import TokenService

"""
TokenServiceImpl is an implementation of the TokenService interface.
"""
class TokenServiceImpl(TokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

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