import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Query, Request, HTTPException
from fastapi.responses import JSONResponse

import httpx

from services.iot_service import IOTService
from models.request import SensorRequest

router = APIRouter()

@router.post('/on')
async def turn_on(request: Request):
    async with httpx.AsyncClient() as client:
        uid = request.state.user_id
        iot_server_url = os.getenv("IOT_SERVER_URL")
        iot_servet_port = os.getenv("IOT_SERVER_PORT")

        response = await client.post(f"{iot_server_url}:{iot_servet_port}/start_system", json={"user_id": uid})
        CustomLogger().get_logger().info(f"Turn On IOT-system response: {response}")

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
        CustomLogger().get_logger().info(f"Turn Off IOT-system response: {response}")

        if response.status_code == 200:
            return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to stop system")

@router.get('/status')
async def get_status():
    pass

@router.get('/data')
async def get_sensor_data(
    request: Request,
    sensor_type: str = Query(..., description="Sensor type. e.g. temperature(temp), humidity(hum)"),
    amt: int = Query(..., description="Amount of data to retrieve")
):
    uid = request.state.user_id

    if not sensor_type or not amt:
        raise HTTPException(status_code=400, detail="Invalid sensor request")

    try:
        sensor_request = SensorRequest(sensor_type=sensor_type, amt=amt)
        data = IOTService()._get_sensor_data(uid, sensor_request)
        CustomLogger().get_logger().info(f"Request data for {sensor_type} : {amt} get {data.count()} response data.")

        return JSONResponse(
            content=data,
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get('/all_data')
async def get_all_sensor_data(request: Request):
    uid = request.state.user_id

    try:
        data = IOTService()._get_all_sensors_data(uid)
        CustomLogger().get_logger().info(f"Request all_data get {data.__len__()} response data.")
        for sensor_data in data:
            if 'timestamp' in sensor_data:
                sensor_data['timestamp'] = sensor_data['timestamp'].isoformat()
            
        return JSONResponse(
            content=data,
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post('/slider1')
async def post_slider1_data(request: Request):
    uid = request.state.user_id
    data = await request.json()

    CustomLogger().get_logger().info(f"Received slider1 data: {data}")

    slider_data = {
        "uid": str(uid),
        "device_type": "headlight",
        "value": float(data["max"]),
    }

    if 'min' not in data or 'max' not in data:
        raise HTTPException(status_code=400, detail="Invalid slider2 data")

    try:
        # Assuming _send_slider_data can handle min and max values
        IOTService()._send_slider_data(uid, slider_data)
        return JSONResponse(content={"message": "Slider1 values sent successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post('/slider2')
async def post_slider2_data(response: JSONResponse, request: Request):
    uid = request.state.user_id
    data = await request.json()

    CustomLogger().get_logger().info(f"Received slider2 data: {data}")

    slider_data = {
        "uid": str(uid),
        "device_type": "airconditioner",
        "value": float(data["max"]),
    }

    if 'min' not in data or 'max' not in data:
        raise HTTPException(status_code=400, detail="Invalid slider2 data")

    try:
        # Assuming _send_slider_data can handle min and max values
        IOTService()._send_slider_data(uid, slider_data)
        return JSONResponse(content={"message": "Slider2 values sent successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    
