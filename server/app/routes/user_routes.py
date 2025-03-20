from fastapi import APIRouter, HTTPException, Request, Response

from models.request import UserInfoRequest
from services.user_service import UserService

router = APIRouter()

@router.get("/user")
async def get_user_info(request: Request):
    uid = request.state.user_id
    user = UserService()._get_user_info(uid)
    
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")