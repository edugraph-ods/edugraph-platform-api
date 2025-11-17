from pydantic import BaseModel

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