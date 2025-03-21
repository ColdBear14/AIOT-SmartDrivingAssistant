from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

from services.sensor_service import SensorService

router = APIRouter()

@router.post('/on')
async def turn_on(request: Request):
    pass

@router.post('/off')
async def turn_off(request: Request):
    pass

@router.get('/status')
async def get_status():
    pass

@router.get('/')
async def get_sensor_data(request: Request):
    uid = request.state.user_id

    try:
        data = SensorService()._get_sensor_data(uid, request)

        if data:
            return JSONResponse(
                content=data,
                status_code=200
            )
        else:
            raise HTTPException(status_code=404, detail="Data not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")