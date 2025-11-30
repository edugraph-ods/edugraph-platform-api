from pydantic import BaseModel, EmailStr, Field


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    newPassword: str = Field(min_length=8, max_length=128)
