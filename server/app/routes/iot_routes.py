import os
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Request, Depends, WebSocket
from fastapi.responses import JSONResponse

from services.iot_service import IOTService
from services.user_service import UserService
from models.request import ControlServiceRequest

router = APIRouter()

def get_user_id(request: Request) -> str: 
    return request.state.user_id

@router.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str = None):
    if device_id is None:
        await websocket.close(code=1008, reason="Device ID is required")
        return
    
    if websocket is None:
        await websocket.close(code=1008, reason="WebSocket is required")
        return
    
    CustomLogger()._get_logger().info(f"WebSocket connect request from: {device_id}")
    
    check_user = UserService()._check_user_exist(device_id)
    if not check_user:
        await websocket.close(code=1008, reason="User not found for device ID")
        return
    
    try:
        await IOTService()._establish_connection(device_id, websocket)

    except Exception as e:
        CustomLogger()._get_logger().error(f"Websocket error: {e}")
        await websocket.close(code=1011, reason="Internal server error")

@router.post('/on')
async def turn_on(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)

    try:
        await IOTService()._control_iot_system(
            device_id=uid,
            target="system",
            command="on"
        )
        
        return JSONResponse(content={"message": "System started successfully"}, status_code=200)
            
    except Exception as e:
        return JSONResponse(content={"message": "Failed to start system", "detail": str(e.args[0])}, status_code=500)

@router.post('/off')
async def turn_off(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)
    
    try:
        await IOTService()._control_iot_system(
            device_id=uid,
            target="system",
            command="off"
        )
        
        return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
            
    except Exception as e:
        CustomLogger()._get_logger().error(f"Error stopping system: {e}")
        return JSONResponse(content={"message": "Failed to stop system", "detail": str(e.args[0])}, status_code=500)

@router.patch("/service")
async def control_service(request: ControlServiceRequest, uid = Depends(get_user_id)):
    """
    Send control commands to IoT system websocket.
    """
    try:
        service_type = request.service_type
        value = request.value

        CustomLogger()._get_logger().info(f"Control service: {service_type}, value: {value}")

        await IOTService()._control_iot_system(
            device_id=uid,
            target=service_type,
            command=value
        )
            
        return JSONResponse(
            content={"message": "Service control request processed successfully"},
            status_code=200
        )
            
    except Exception as e:
        return JSONResponse(
            content={"message": "Failed to control service", "detail": str(e.args[0])},
            status_code=500
        )
 