from pydantic import BaseModel, EmailStr

"""
SignInRequest is a class that represents a sign in request.

Attributes:
    email (EmailStr): The email of the user.
    password (str): The password of the user.
"""
class SignInRequest(BaseModel):
    email: EmailStr
    password: str