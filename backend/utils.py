from pymongo import MongoClient
from config import config
from fastapi import Request, HTTPException
from database import db

def get_uid(request: Request):
    session_id = request.cookies.get('session_id')
    users = db.get_user_collection()
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session found")
    
    user = users.find_one({'session_id': session_id})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid session or user not found")

    return user["_id"] 
