from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt

from app.config import settings

"""
create_access_token is a function that creates an access token.

Args:
    data (Dict[str, Any]): The data to encode.
    expires_delta (Optional[timedelta], optional): The time delta for the token to expire. Defaults to None.
    secret_key (Optional[str], optional): The secret key to use. Defaults to None.
    algorithm (Optional[str], optional): The algorithm to use. Defaults to None.

Returns:
    str: The access token.
"""
def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    secret_key: Optional[str] = None,
    algorithm: Optional[str] = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta is not None else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key or settings.secret_key, algorithm=algorithm or settings.algorithm)

"""
decode_access_token is a function that decodes an access token.

Args:
    token (str): The access token to decode.
    secret_key (Optional[str], optional): The secret key to use. Defaults to None.
    algorithm (Optional[str], optional): The algorithm to use. Defaults to None.

Returns:
    Dict[str, Any]: The decoded access token.
"""
def decode_access_token(
    token: str,
    secret_key: Optional[str] = None,
    algorithm: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        return jwt.decode(token, secret_key or settings.secret_key, algorithms=[algorithm or settings.algorithm])
    except JWTError:
        return {}
