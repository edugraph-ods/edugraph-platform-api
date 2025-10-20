from pydantic import BaseModel, EmailStr, validator

"""
SignUpRequest is a class that represents a sign up request.

Attributes:
    email (EmailStr): The email of the user.
    password (str): The password of the user.
    full_name (str): The full name of the user.
"""
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None

    @validator("email")
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        allowed_domains = {
            "upc.edu.pe",
            "upn.edu.pe",
            "utp.edu.pe",
            "unmsm.edu.pe",
        }
        domain = value.split("@")[-1]
        if domain not in allowed_domains:
            raise ValueError("email domain is not allowed")
        return value

    @validator("password")
    def validate_password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        return value

"""
SignInRequest is a class that represents a sign in request.

Attributes:
    email (EmailStr): The email of the user.
    password (str): The password of the user.
"""
class SignInRequest(BaseModel):
    email: EmailStr
    password: str

"""
AuthResponse is a class that represents an authentication response.

Attributes:
    access_token (str): The access token.
    token_type (str): The token type.
    user_id (int): The user id.
    email (str): The email of the user.
"""
class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str

"""
TokenData is a class that represents a token data.

Attributes:
    user_id (int): The user id.
    email (str): The email of the user.
"""
class TokenData(BaseModel):
    user_id: int = None
    email: str = None