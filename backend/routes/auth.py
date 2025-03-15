from fastapi import APIRouter, Depends
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
async def login(user: UserRequest, users=Depends(get_user_collection)):
    user = User(user.username, user.password)
    return user.authenticate(users)