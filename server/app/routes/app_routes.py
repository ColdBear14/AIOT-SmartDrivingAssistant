import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from services.app_service import AppService
from models.request import ActionHistoryRequest, SensorDataRequest

router = APIRouter()

def get_user_id(request: Request) -> str: 
    return request.state.user_id

@router.get('/sensor_data')
async def get_sensor_data(
    sensor_types: str,  # Receive as comma-separated string
    uid: str = Depends(get_user_id)
):
    if not sensor_types:
        return JSONResponse(content=[], status_code=200)
    
    try:
        # Split the comma-separated string and create the request object
        sensor_types_list = [s.strip() for s in sensor_types.split(',')]
        request = SensorDataRequest(sensor_types=sensor_types_list)
        
        data = AppService()._get_sensors_data(uid, request)

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
        return JSONResponse(
            content={"message": "Internal server error ", "detail": str(e)},
            status_code=500
        )

@router.get("/services_status")
async def get_services_status(uid = Depends(get_user_id)):
    """
    Endpoint to get all services config information includes mode and value.
    """
    try:
        service_config_data = AppService()._get_services_status(uid)

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

# @router.patch("/config")
# async def update_service_config(request: ServiceConfigRequest, uid = Depends(get_user_id)):
#     """
#     Endpoint to update services mode config.
#     """
#     if request is None:
#         return JSONResponse(content={"message": "Invalid request"}, status_code=400)
    
#     try: 
#         AppService()._update_service_config(uid, request)
#         CustomLogger().get_logger().info(f"User config updated: {request}")

#         return JSONResponse(
#             content={"message": "User config updated successfully"},
#             status_code=200,
#             media_type="application/json"
#         )
    
#     except Exception as e:
#         if e.args[0] == "No data to update":
#             return JSONResponse(
#                 content={"message": e.args[0], "detail": "Request contain no data to update"},
#                 status_code=422
#             )
#         elif e.args[0] == "No service config updated":
#             return JSONResponse(
#                 content={"message": e.args[0], "detail": "Can not find any document with the uid that extracted from cookie's session"},
#                 status_code=404
#             )
#         else:
#             return JSONResponse(
#                 content={"message": "Internal server error ", "detail": e.args[0]},
#                 status_code=500
#             )

@router.get("/action_history")
async def get_action_history(request: ActionHistoryRequest, uid = Depends(get_user_id)):
    try:
        data = AppService()._get_action_history(uid, request)

        CustomLogger().get_logger().info(f"Retrieved action history for {request.service_type} of user {uid}")

        return JSONResponse(
            content=data,
            status_code=200
        )
    
    except Exception as e:
        return JSONResponse(
            content={"message": "Internal server error ", "detail": e.args[0]},
            status_code=500
        )