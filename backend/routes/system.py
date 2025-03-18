from pymongo.collection import Collection
from fastapi import APIRouter, Request, Depends, HTTPException
from services.iot import IOTSystem
from utils.utils import get_collection
router = APIRouter()

iot_system = IOTSystem()
def get_user_collection():
    return get_collection('user')

def get_sensor_collection():
    return get_collection('environment_sensor')

@router.post('/on')
async def turn_on(request: Request, users=Depends(get_user_collection)):
    session_id = request.cookies.get('session_id')
    if not session_id:
        raise HTTPException(status_code=400, detail="No active session found")
    
    user = users.find_one({'session_id': session_id})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid session or user not found")

    uid = user["_id"]  # Now it's safe to access '_id'

    iot_system.start_system(uid)
    
    return {"message": "System turned ON"}

@router.post('/off')
async def turn_off():
    iot_system.stop()
    return {"message": "System turned OFF"}