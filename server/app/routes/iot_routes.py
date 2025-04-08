import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Query, Request, Depends
from fastapi.responses import JSONResponse

import httpx

from services.iot_service import IOTService
from models.request import ControlServiceRequest, SensorDataRequest, ServiceConfigRequest

router = APIRouter()

def get_user_id(request: Request) -> str: 
    return request.state.user_id

@router.post('/on')
async def turn_on(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)

    async with httpx.AsyncClient() as client:
        iot_server_url = os.getenv("IOT_SERVER_URL")
        iot_servet_port = os.getenv("IOT_SERVER_PORT")

        response = await client.post(f"{iot_server_url}:{iot_servet_port}/start_system", json={"user_id": uid})
        CustomLogger().get_logger().info(f"Turn On IOT-system response: {response}")

        if response.status_code == 200:
            return JSONResponse(content={"message": "System started successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Failed to start system"}, status_code=500)

@router.post('/off')
async def turn_off(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)
    
    async with httpx.AsyncClient() as client:
        iot_server_url = os.getenv("IOT_SERVER_URL")
        iot_servet_port = os.getenv("IOT_SERVER_PORT")

        response = await client.post(f"{iot_server_url}:{iot_servet_port}/stop_system")
        CustomLogger().get_logger().info(f"Turn Off IOT-system response: {response}")

        if response.status_code == 200:
            return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Failed to stop system"}, status_code=500)

@router.get('/status')
async def get_status():
    pass

@router.get('/data')
async def get_sensor_data(
    request: SensorDataRequest = None,
    uid: str = Depends(get_user_id)
):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)

    try:
        data = IOTService()._get_sensor_data(uid, request)

        for sensor_data in data:
            if 'timestamp' in sensor_data:
                sensor_data['timestamp'] = sensor_data['timestamp'].isoformat()

        sensor_types_str = ', '.join(request.sensor_types)
        CustomLogger().get_logger().info(f"Retrieved data for {sensor_types_str} types.")

        return JSONResponse(
            content=data,
            status_code=200
        )
    except Exception as e:
        if e.args[0] == "No data found":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message":  "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

@router.get("/config")
async def get_user_config(uid = Depends(get_user_id)):
    """
    Endpoint to get all services config information includes mode and value.
    """
    try:
        service_config_data = IOTService()._get_service_config(uid)

        CustomLogger().get_logger().info(f"User config: {service_config_data}")

        return JSONResponse(
            content=service_config_data,
            status_code=200,
            media_type="application/json"
        )
        
    except Exception as e:
        if e.args[0] == "Service config not find":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message": "Internal server error ", "detail": e.args[0]},
                status_code=500
            )

@router.patch("/config")
async def update_service_config(request: ServiceConfigRequest, uid = Depends(get_user_id)):
    """
    Endpoint to update services mode config.
    """
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)
    
    try: 
        IOTService()._update_service_config(uid, request)
        CustomLogger().get_logger().info(f"User config updated: {request}")

        return JSONResponse(
            content={"message": "User config updated successfully"},
            status_code=200,
            media_type="application/json"
        )
    
    except Exception as e:
        if e.args[0] == "No data to update":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Request contain no data to update"},
                status_code=422
            )
        elif e.args[0] == "No service config updated":
            return JSONResponse(
                content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
                status_code=404
            )
        else:
            return JSONResponse(
                content={"message": "Internal server error ", "detail": e.args[0]},
                status_code=500
            )
        
@router.patch("/service")
async def control_service(request: ControlServiceRequest, uid = Depends(get_user_id)):
    """
    Redirect to IoT system's endpoint to control services value base on current mode.
    """
    pass
    
@router.post('/slider')
async def post_data(request: Request):
    uid = request.state.user_id
    data = await request.json()
    CustomLogger().get_logger().info(f"Received slider data: {data}")

    if 'slider_value' not in data:
        return JSONResponse(content={"message": "Invalid slider data"}, status_code=400)

    try:
        IOTService()._send_slider_data(uid, data['slider_value'])
        return JSONResponse(content={"message": "Slider value sent successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to send slider value"}, status_code=500)
    
