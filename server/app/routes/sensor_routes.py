from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.params import Body

from utils.utils import get_uid
from models.request import SensorRequest
from services.database import Database

router = APIRouter()

@router.get('/sensor_data')
async def get_sensor_data(
    request: Request,
    sensor_request: SensorRequest = Body(...),
    sensors_collection=Depends(Database()._instance.get_sensor_collection)
):
    uid = get_uid(request=request)
    if not uid:
        return {'message': 'Invalid session or user not found'}
    if not sensors_collection:
        return {'message': 'Sensor collection not found'}

    result = await sensors_collection.find({'uid': uid}).to_list(length=sensor_request.amt)

    print(result)
    return {'data': result}

@router.get('/sensor_data_all')
async def get_all_sensor_data(sensors_collection=Depends(Database()._instance.get_sensor_collection)):
    result = await sensors_collection.find().to_list(length=100)
    for doc in result:
        print(doc)
    return {'data': "All sensor data"}


