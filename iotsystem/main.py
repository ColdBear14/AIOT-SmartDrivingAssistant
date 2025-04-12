import sys
import os

from fastapi.responses import JSONResponse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger
from iotsystem.services.iot import IOTSystem
from iotsystem.models.request import UserIdRequest, ControlServiceRequest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc thay "*" bằng frontend URL, ví dụ: ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (POST, GET, OPTIONS, ...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)
@app.post("/start_system")
async def start_system(uid_request: UserIdRequest):
    await IOTSystem()._instance.start_system(uid_request.user_id)
    CustomLogger().get_logger().info("System turned ON")
    return JSONResponse(content={"message": "System started successfully"}, status_code=200)

@app.post("/stop_system")
async def stop_system():
    await IOTSystem()._instance.stop_system()
    CustomLogger().get_logger().info("System turned OFF")
    return JSONResponse(content={"message": "System stopped successfully"}, status_code=200)

@app.post("/service")
async def control_service(request: ControlServiceRequest):
    try:
        print(request)
        success = await IOTSystem()._instance.control_service(
            request.user_id,
            request.service_type,
            request.value
        )

        if success:
            CustomLogger().get_logger().info(f"Service {request.service_type} controlled successfully")

            return JSONResponse(
                content={"message": "Service controlled successfully"},
                status_code=200
            )
        
        else:
            CustomLogger().get_logger().info(f"Failed to control service {request.service_type}")
            return JSONResponse(
                content={"message": "Failed to control service"},
                status_code=500
            )
        
    except Exception as e:
        CustomLogger().get_logger().error(f"Error controlling service: {e}")
        return JSONResponse(
            content={"message": "Internal server error", "detail": "Error controlling service"},
            status_code=500
        )

if __name__ == '__main__':
    import uvicorn
    CustomLogger().get_logger().info("App: __main__")
    uvicorn.run("iotsystem.main:app", host='0.0.0.0', port=8000,reload=True)