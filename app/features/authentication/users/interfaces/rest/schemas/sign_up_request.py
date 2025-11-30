from pydantic import BaseModel, EmailStr, validator

"""
SignUpRequest is a class that represents a sign up request.

Attributes:
    email (EmailStr): The email of the user.
    password (str): The password of the user.
"""
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @validator("email")
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        domain = value.split("@")[-1]
        if not domain.endswith(".edu.pe"):
            raise ValueError("email domain is not allowed. Only institutional .edu.pe domains are permitted")
        return value

    @validator("password")
    def validate_password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        return value