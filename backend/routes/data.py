from fastapi import APIRouter, Depends, Request
from utils.utils import get_collection, get_uid
from models.request import SensorRequest
router = APIRouter()

def get_sensor_collection():
    return get_collection('environment_sensor')
def get_user_collection():
    return get_collection('user')

@router.post('/sensor_data')
async def get_sensor_data(sensor:SensorRequest,request: Request,sensors_collection=Depends(get_sensor_collection)):
    uid = get_uid(request=request)
    
    sensors_collection.find({'uid': uid})