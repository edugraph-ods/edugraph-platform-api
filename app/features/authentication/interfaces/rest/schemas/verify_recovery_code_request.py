from pydantic import BaseModel, EmailStr, Field


class VerifyRecoveryCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=1)
