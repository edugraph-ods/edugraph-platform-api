from pydantic import BaseModel
from pydantic import EmailStr

"""
AuthResponse represents the payload returned after a successful sign-in.
"""
class AuthResponse(BaseModel):
    token: str
    userId: str
    email: EmailStr
    username: str
    accountId: str


class ProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr