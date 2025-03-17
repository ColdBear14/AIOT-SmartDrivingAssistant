from fastapi import APIRouter, Depends, Request
from utils import get_collection, get_uid
from models import SensorRequest
router = APIRouter()

def get_sensor_collection():
    return get_collection('environment_sensor')
def get_user_collection():
    return get_collection('user')

@router.post('/sensor_data')
async def get_sensor_data(sensor:SensorRequest,request: Request,sensors_collection=Depends(get_sensor_collection)):
    uid = get_uid(request=request)
    
    sensor_data = list(sensors_collection.find({'uid': uid,'sensor_type': sensor.sensor_type}).limit(sensor.amt))
    
    return {'sensor_data':sensor_data, 'message': 'Retrieve sensor data successful'}