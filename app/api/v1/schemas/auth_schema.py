from pydantic import BaseModel, EmailStr, validator

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

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str

class TokenData(BaseModel):
    user_id: int = None
    email: str = None