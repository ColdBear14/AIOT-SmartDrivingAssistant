from fastapi import APIRouter, Depends, Request
from utils.utils import get_collection, get_uid
from models.request import SensorRequest
router = APIRouter()
from services.database import Database
db = Database()._instance

@router.post('/sensor_data')
async def get_sensor_data(sensor:SensorRequest,request: Request,sensors_collection=Depends(db.get_sensor_collection)):
    uid = get_uid(request=request)
    
    sensors_collection.find({'uid': uid})