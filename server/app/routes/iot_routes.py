import os

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

import httpx

from services.sensor_service import SensorService

router = APIRouter()

@router.post('/on')
async def turn_on(request: Request):
    async with httpx.AsyncClient() as client:
        uid = request.state.user_id
        iot_server_url = os.getenv("IOT_SERVER_URL")
        iot_servet_port = os.getenv("IOT_SERVER_PORT")

        response = await client.post(f"{iot_server_url}:{iot_servet_port}/start_system", json={"user_id": uid})

        if response.status_code == 200:
            return JSONResponse(content={"message": "System started successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to start system")

@router.post('/off')
async def turn_off(request: Request):
    async with httpx.AsyncClient() as client:
        uid = request.state.user_id
        iot_server_url = os.getenv("IOT_SERVER_URL")
        iot_servet_port = os.getenv("IOT_SERVER_PORT")

        response = await client.post(f"{iot_server_url}:{iot_servet_port}/stop_system")

        if response.status_code == 200:
            return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to stop system")

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