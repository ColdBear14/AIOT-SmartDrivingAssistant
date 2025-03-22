# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, HTTPException, Request, Response
from starlette.responses import JSONResponse

from models.request import UserRequest
from services.auth_service import AuthService

router = APIRouter()

@router.post("/register")
async def register(user: UserRequest):
    if not user or not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Invalid request")
    
    try:
        result = AuthService()._register(user)
        CustomLogger().get_logger().info(f"Register result: {result}")

        if result:
            return JSONResponse(
                content={"message": "User created successfully"},
                status_code=201
            )
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        if e.args[0] == "Username already exists":
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/login")
async def login(user: UserRequest, response: Response):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Invalid request")

    try:
        session_id, userid = AuthService()._authenticate(user)
        CustomLogger().get_logger().info(f"Login result: {session_id} - {userid}")

        if session_id:
            response = JSONResponse(
                content={"message": "Login successful"},
                status_code=200
            )
            response = AuthService()._add_cookie(response, session_id)
            
            return response
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        if e.args[0] == "Invalid credentials":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session found")

    try:
        result = AuthService()._del_session(session_id)
        CustomLogger().get_logger().info(f"Logout result: {result}")
        if result:
            response = JSONResponse(
                content={"message": "Logout successful"},
                status_code=200
            )
            response.delete_cookie("session_id")  # Delete cookie from client
            return response
        else:
            raise HTTPException(status_code=500, detail="Session not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

