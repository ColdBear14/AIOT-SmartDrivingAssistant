import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

import httpx

from services.iot_service import IOTService
from models.request import ControlServiceRequest

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

@router.get("/connection")
async def get_connection_detail(uid = Depends(get_user_id)):
    pass

@router.put("/connection")
async def update_connection_detail(uid = Depends(get_user_id)):
    pass

@router.patch("/service")
async def toggle_service(request: ControlServiceRequest, uid = Depends(get_user_id)):
    """
    Redirect to IoT system's endpoint to control services value base on current mode.
    """
    try:
        service_data = request.dict(exclude_unset=True)
        success = False
        
        for service_name, value in service_data.items():
            # Convert names like air_cond_temp to air_cond_service
            service_type = service_name.replace('_temp', '_service').replace('_brightness', '_service').replace('_threshold', '_service')

            CustomLogger().get_logger().info(f"Control service: {service_type}, value: {value}")

            result = await IOTService()._control_service(uid, service_type, value)
            success = success or result
            
        if success:
            return JSONResponse(
                content={"message": "Service control request processed successfully"},
                status_code=200
            )
        else:
            return JSONResponse(
                content={"message": "Failed to control service"},
                status_code=500
            )
            
    except Exception as e:
        CustomLogger().get_logger().error(f"Error controlling service: {e}")
        return JSONResponse(
            content={"message": "Internal server error", "detail": str(e)},
            status_code=500
        )

@router.post('/slider')
async def slider_data(request: Request):
    uid = request.state.user_id
    data = await request.json()

    CustomLogger().get_logger().info(f"Received slider data: {data}")

    if  'max' not in data:
        CustomLogger().get_logger().error("Value is missing in the request data")
        return JSONResponse(content={"message": "Value is missing"}, status_code=400)

    try:
        
        service_type = data.get('name')
        value = data.get('max')


        # Assuming _send_slider_data can handle min and max values
        IOTService()._control_service(uid, service_type, value)
        return JSONResponse(content={"message": "Slider values sent successfully"}, status_code=200)
    except Exception as e:
        CustomLogger().get_logger().error(f"Error sending slider data: {e}")
        return JSONResponse(content={"message": "Internal server error"}, status_code=500)