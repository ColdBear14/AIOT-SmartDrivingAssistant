import sys
import os
# Add the root path to the sys.path to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from utils.custom_logger import CustomLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middlewares.auth_middleware import AuthMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:9000"],  # First one is app client, second one is iot-server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(AuthMiddleware)

from routes.auth_routes import router as auth_router
app.include_router(auth_router, prefix='/auth')

from routes.user_routes import router as user_router
app.include_router(user_router, prefix='/user')

from routes.iot_routes import router as iot_router
app.include_router(iot_router, prefix='/iot')

for route in app.routes:
    CustomLogger().get_logger().info(route)

if __name__ == '__main__':
    CustomLogger().get_logger().info("main: __main__")

    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)