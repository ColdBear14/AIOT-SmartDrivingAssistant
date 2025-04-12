import os
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from services.iot_service import IOTService
from services.mqtt_service import MQTTService
from models.request import ControlServiceRequest

router = APIRouter()

def get_user_id(request: Request) -> str: 
    return request.state.user_id

@router.post('/on')
async def turn_on(request: Request, uid: str = Depends(get_user_id)):
    if request is None:
        return JSONResponse(content={"message": "Invalid request"}, status_code=400)

    try:
        mqtt_service = MQTTService()
        success = mqtt_service.send_control_command(uid, {"command": "start_system"})
        
        if success:
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
        mqtt_service = MQTTService()
        success = mqtt_service.send_control_command(uid, {"command": "stop_system"})
        
        if success:
            return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Failed to stop system"}, status_code=500)
            
    except Exception as e:
        CustomLogger().get_logger().error(f"Error stopping system: {e}")
        return JSONResponse(content={"message": "Failed to stop system", "detail": str(e)}, status_code=500)

@router.get("/connection")
async def get_connection_detail(uid = Depends(get_user_id)):
    pass

@router.put("/connection")
async def update_connection_detail(uid = Depends(get_user_id)):
    pass

@router.patch("/service")
async def control_service(request: ControlServiceRequest, uid = Depends(get_user_id)):
    """
    Send control commands to IoT system via MQTT.
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