# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from models.request import UserInfoRequest
from services.user_service import UserService

router = APIRouter()

@router.get("/")
async def get_user_info(request: Request):
    uid = request.state.user_id

    try:
        user = UserService()._get_user_info(uid)
        if user:
            data = {}
            for key in UserService().ALL_FIELDS:
                if key in user:
                    data[key] = user[key]
            CustomLogger().get_logger().info(f"User info: {data}")

            return JSONResponse(
                content=data,
                status_code=200,
                media_type="application/json"
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
        
    except Exception as e:
        if e.type == "ValueError":
            raise HTTPException(status_code=500, detail="Cannot extract user info from request's cookies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/")
async def update_user_info(request: Request, user_info_request: UserInfoRequest):
    uid = request.state.user_id

    try:
        UserService()._update_user_info(uid, user_info_request)
        CustomLogger().get_logger().info(f"User info updated: {user_info_request}")

        return JSONResponse(
            content={"message": "User info updated successfully"},
            status_code=200,
            media_type="application/json"
        )
    
    except Exception as e:
        if e.type == "ValueError":
            if e.args[0] == "No valid fields to update":
                raise HTTPException(status_code=400, detail="No valid fields to update")
            elif e.args[0] == "No user info updated":
                raise HTTPException(status_code=400, detail="No user info updated")
            else:
                raise HTTPException(status_code=500, detail="Cannot extract user info from request's cookies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/")
async def delete_user_info(request: Request):
    uid = request.state.user_id

    try:
        UserService()._delete_user_info(uid)
        CustomLogger().get_logger().info(f"User info deleted: {uid}")
        
        response = JSONResponse(
            content={},
            status_code=204
        )
        response.delete_cookie("session_id")
        return response
    
    except Exception as e:
        if e.type == "ValueError":
            raise HTTPException(status_code=500, detail="Cannot extract user info from request's cookies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")