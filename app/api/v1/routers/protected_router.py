from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_active_user
from app.core.entities.user import User

router = APIRouter(prefix="/protected", tags=["protected"])

"""
_protected_route is a function that returns a protected route.

Args:
    current_user (User): The current user.

Returns:
    dict: The protected route.
"""
@router.get("/route")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.email}"}

"""
_get_profile is a function that returns the profile of the current user.

Args:
    current_user (User): The current user.

Returns:
    dict: The profile of the current user.
"""
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
