from fastapi import APIRouter, Depends,Response, HTTPException, Request
from utils import get_collection
from models import User, UserRequest

router = APIRouter()

def get_user_collection():
    return get_collection("user") 

@router.post("/register")
async def register(user: UserRequest, users=Depends(get_user_collection)):
    user = User(user.username, user.password)
    return user.save(users)

@router.post("/login")
async def login(user: UserRequest, response: Response, users=Depends(get_user_collection)):
    user = User(user.username, user.password)
    session_id = user.authenticate(users) 
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600
    )
    
    return {'message': 'Login successful'}

@router.post("/logout")
async def logout(request: Request, response: Response, users=Depends(get_user_collection)):
    session_id = request.cookies.get("session_id") 
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session found")

    result = users.update_one({"session_id": session_id}, {"$unset": {"session_id": ""}})
    
    response.delete_cookie("session_id")  # Delete cookie from client

    return {"message": "Logged out successfully"}