from fastapi import APIRouter, Depends
from utils import get_collection
from models import User

router = APIRouter()

def get_user_collection():
    return get_collection("user") 

@router.post("/register")
async def register(username: str, password: str, users=Depends(get_user_collection)):
    user = User(username, password)
    return user.save(users)

@router.post("/login")
async def login(username: str, password: str, users=Depends(get_user_collection)):
    user = User(username, password)
    return user.authenticate(users)