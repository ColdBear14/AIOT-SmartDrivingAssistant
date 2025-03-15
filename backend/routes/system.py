from fastapi import APIRouter
from iot import IOTSystem
router = APIRouter()

iot_system = IOTSystem()
@router.post('/on')
def turn_on():
    iot_system.start_system()
    return {"message": "System turned ON"}
@router.post('/off')
def turn_off():
    iot_system.stop_system()
    return {"message": "System turned OFF"}