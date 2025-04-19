from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Request, Response
from starlette.responses import JSONResponse

from pymongo.errors import PyMongoError

from services.auth_service import AuthService

from models.request import UserRequest

router = APIRouter()

@router.post("/register")
async def register(user: UserRequest):
    try:
        result = AuthService()._register(user)
        CustomLogger()._get_logger().info(f"Register result: {result}")

        if result:
            return JSONResponse(
                content={"message": "User created successfully"},
                status_code=201
            )
        else:
            return JSONResponse(
                content={"message": "User not created"},
                status_code=500
            )

    except Exception as e:
        CustomLogger()._get_logger().error(f"Failed to register user: {e.args[0]}")
        if e.__class__ == PyMongoError:
            # raise HTTPException(status_code=500, detail="Can not operate database transaction")
            return JSONResponse(
                content={"message": "Can not operate database transaction"},
                status_code=500
            )
        elif e.args[0] == "Username already exists":
            return JSONResponse(
                content={"message": "Username already exists"},
                status_code=409
            )
        else:
            return JSONResponse(
                content={"message": "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

@router.patch("/login")
async def login(user: UserRequest, response: Response):
    try:
        session_id, userid = AuthService()._authenticate(user)
        CustomLogger()._get_logger().info(f"Login result: {session_id} - {userid}")

        if session_id:
            response = JSONResponse(
                content={"message": "Login successful"},
                status_code=200
            )
            response = AuthService()._add_cookie_session(response, session_id)
            
            return response
        else:
            return JSONResponse(
                content={"message": "Failed to create session"},
                status_code=401
            )

    except Exception as e:
        CustomLogger()._get_logger().error(f"Failed to login user: {e.args[0]}")
        if e.args[0] == "Invalid credentials":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Invalid username or password"},
                status_code=401
            )
        else:
            return JSONResponse(
                content={"message": "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

@router.patch("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return JSONResponse(
            content={"message": "Unauthorized: Missing session token"},
            status_code=401
        )

    try:
        result = AuthService()._del_session(session_id)
        CustomLogger()._get_logger().info(f"Logout result: {result}")
        if result:
            response = JSONResponse(
                content={"message": "Logout successful"},
                status_code=200
            )
            # response.delete_cookie("session_id")
            response = AuthService()._del_cookie_session(response)

            return response
        else:
            return JSONResponse(
                content={"message": "Failed to delete session"},
                status_code=500
            )
    
    except Exception as e:
        CustomLogger()._get_logger().error(f"Failed to logout user: {e.args[0]}")
        return JSONResponse(
            content={"message": "Internal server error ", "detail": e.args[0]},
            status_code=500
        )

