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
        return JSONResponse(content={"message": "Device ID is required"}, status_code=400)
    
    if websocket is None:
        return JSONResponse(content={"message": "WebSocket is required"}, status_code=400)
    
    CustomLogger().get_logger().info(f"WebSocket connect request from: {device_id}")
    
    check_user = UserService()._check_user_exist(device_id)
    if not check_user:
        return JSONResponse(
            content={
                "message": "User not find",
                "detail": "Can not find any user for that device id"
            },
            status_code=404
        )
    
    try:
        await IOTService()._establish_connection(device_id, websocket)

    except Exception as e:
        CustomLogger().get_logger().error(f"Websocket error: {e}")

@router.post('/on')
async def turn_on(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)

    try:
        result = await IOTService()._control_iot_system(uid, "system", "on")
        
        if result:
            return JSONResponse(content={"message": "System started successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Failed to start system"}, status_code=500)
            
    except Exception as e:
        CustomLogger().get_logger().error(f"Error starting system: {e}")
        return JSONResponse(content={"message": "Failed to start system", "detail": str(e)}, status_code=500)

@router.post('/off')
async def turn_off(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)
    
    try:
        result = await IOTService()._control_iot_system(uid, "system", "off")
        
        if result:
            return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Failed to stop system"}, status_code=500)
            
    except Exception as e:
        CustomLogger().get_logger().error(f"Error stopping system: {e}")
        return JSONResponse(content={"message": "Failed to stop system", "detail": str(e)}, status_code=500)

@router.patch("/service")
async def control_service(request: ControlServiceRequest, uid = Depends(get_user_id)):
    """
    Send control commands to IoT system websocket.
    """
    try:
        service_type = request.service_type
        value = request.value

        CustomLogger().get_logger().info(f"Control service: {service_type}, value: {value}")

        result = await IOTService()._control_iot_system(uid, service_type, value)
            
        if result:
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
 