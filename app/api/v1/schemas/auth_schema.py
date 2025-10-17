from pydantic import BaseModel, EmailStr, validator

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None

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