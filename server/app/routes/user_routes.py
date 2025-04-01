from utils.custom_logger import CustomLogger

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from services.user_service import UserService

from models.request import UserInfoRequest, UserConfigRequest

router = APIRouter()

def get_user_id(request: Request) -> str: 
    return request.state.user_id

@router.get("/")
async def get_user_info(uid = Depends(get_user_id)):
    try:
        user_data = UserService()._get_user_info(uid)

        CustomLogger().get_logger().info(f"User info: {user_data}")

        return JSONResponse(
            content=user_data,
            status_code=200,
            media_type="application/json"
        )
            
        
    except Exception as e:
        if e.args[0] == "User not find":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        elif e.args[0] == "Invalid string to ObjectId conversion":
            return JSONResponse(
                content={"message":  e.args[0], "detail": "Can not extract uid from request's cookie's session"},
                status_code=500
            )
        else:
            return JSONResponse(
                content={"message":  "Internal server error ", "detail": e.args[0]},
                status_code=500
            )
    
@router.patch("/")
async def update_user_info(user_info_request: UserInfoRequest, uid = Depends(get_user_id)):
    try:
        UserService()._update_user_info(uid, user_info_request)
        CustomLogger().get_logger().info(f"User info updated: {user_info_request}")

        return JSONResponse(
            content={"message": "User info updated successfully"},
            status_code=200,
            media_type="application/json"
        )
    
    except Exception as e:
        if e.args[0] == "No data to update":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Request contain no data to update"},
                status_code=422
            )
        elif e.args[0] == "No user info updated":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message":  "Internal server error ", "detail": e.args[0]},
                status_code=500
            )
    
@router.delete("/")
async def delete_user_info(uid = Depends(get_user_id)):
    try:
        UserService()._delete_user_account(uid)
        CustomLogger().get_logger().info(f"User info deleted: {uid}")
        
        response = JSONResponse(
            content={},
            status_code=204
        )
        response.delete_cookie("session_id")
        return response
    
    except Exception as e:
        return JSONResponse(
            content={"message": "Internal server error ", "detail": e.args[0]},
            status_code=500
        )
        
@router.get("/avatar")
async def get_user_avatar():
    pass

@router.put("/avatar")
async def update_user_avatar():
    pass

@router.delete("/avatar")
async def delete_user_avatar():
    pass

@router.get("/config")
async def get_user_config(uid = Depends(get_user_id)):
    try:
        user_config_data = UserService()._get_user_config(uid)

        CustomLogger().get_logger().info(f"User config: {user_config_data}")

        return JSONResponse(
            content=user_config_data,
            status_code=200,
            media_type="application/json"
        )
        
    except Exception as e:
        if e.args[0] == "User config not find":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message":  "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

@router.patch("/config")
async def update_user_config(user_config_request: UserConfigRequest, uid = Depends(get_user_id)):
    try: 
        UserService()._update_user_config(uid, user_config_request)
        CustomLogger().get_logger().info(f"User config updated: {user_config_request}")

        return JSONResponse(
            content={"message": "User config updated successfully"},
            status_code=200,
            media_type="application/json"
        )
    
    except Exception as e:
        if e.args[0] == "No data to update":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Request contain no data to update"},
                status_code=422
            )
        elif e.args[0] == "No user config updated":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message":  "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

