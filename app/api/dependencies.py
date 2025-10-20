from fastapi import Depends
from app.api.v1.routers.auth_router import get_current_user
from fastapi import HTTPException

"""
get_current_active_user is a function that gets the current active user.

Args:
    current_user (User): The current user.

Returns:
    User: The current user.
"""
def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user