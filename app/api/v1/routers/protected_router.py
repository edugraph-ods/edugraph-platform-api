from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_active_user
from app.core.entities.user import User

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/route")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.email}"}

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
