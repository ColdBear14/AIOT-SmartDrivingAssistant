from fastapi import APIRouter, HTTPException, Request, Response

from models.request import UserRequest
from services.auth_service import AuthService

router = APIRouter()

@router.post("/register")
async def register(user: UserRequest):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Invalid request")
    
    try:
        result = AuthService()._register(user)
        
        if result:
            return {"message": "User created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        if e.args[0] == "Username already exists":
            raise HTTPException(status_code=400, detail="Username already exists")
        elif e.args[0] == "UserRequest object is required":
            raise HTTPException(status_code=400, detail="UserRequest object is required")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
async def login(user: UserRequest, response: Response):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Invalid request")

    try:
        session_id, user = AuthService()._authenticate(user)
        if session_id:
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=3600
            )
            
            return {'message': 'Login successful', 'data': user}
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        if e.args[0] == "Invalid credentials":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        elif e.args[0] == "UserRequest object is required":
            raise HTTPException(status_code=400, detail="UserRequest object is required")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")

    try:
        result = AuthService()._del_session(session_id)
        if result:
            response.delete_cookie("session_id")  # Delete cookie from client
            return {"message": "Logged out successfully"}
        else:
            raise HTTPException(status_code=500, detail="Session not found")
    
    except Exception as e:
        if e.args[0] == "Session ID is required":
            raise HTTPException(status_code=400, detail="Session ID is required")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")

