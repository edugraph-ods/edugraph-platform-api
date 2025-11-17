from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

"""
hash_password is a function that hashes the password.

Args:
    password (str): The password to hash.

Returns:
    str: The hashed password.
"""
def hash_password(password: str) -> str:
    return _pwd_context.hash(password)

"""
verify_password is a function that verifies the password.

Args:
    plain_password (str): The plain password.
    hashed_password (str): The hashed password.

Returns:
    bool: True if the password is correct, False otherwise.
"""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return _pwd_context.verify(plain_password, hashed_password)
