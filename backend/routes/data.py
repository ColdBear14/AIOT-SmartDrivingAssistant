from fastapi import APIRouter, Depends
from utils import get_collection
from models import SensorRequest
router = APIRouter()

def get_sensor_collection():
    return get_collection('environment_sensor')
@router.post('/sensor_data')
async def get_sensor_data(sensor:SensorRequest,sensors_collection=Depends(get_sensor_collection)):
    sensors_collection.find()