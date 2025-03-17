from fastapi import APIRouter, Depends, Request
from utils import get_uid
from models import SensorRequest
from database import db
router = APIRouter()

@router.post('/sensor_data')
async def get_sensor_data(sensor:SensorRequest,request: Request,sensors_collection=Depends(db.get_sensor_collection)):
    uid = get_uid(request=request)
    if not uid:
        return {"error": "UID not found", "message": "Unauthorized request"}, 401
    sensor_data = db.find_sensor_data(uid,sensor.sensor_type,sensor.amt)
    
    return {'sensor_data':sensor_data, 'message': 'Retrieve sensor data successful'}