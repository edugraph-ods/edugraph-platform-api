from pydantic import BaseModel
from pydantic import EmailStr

"""
AuthResponse represents the payload returned after a successful sign-in.
"""
class AuthResponse(BaseModel):
    token: str
    userId: str
    email: EmailStr
    name: str