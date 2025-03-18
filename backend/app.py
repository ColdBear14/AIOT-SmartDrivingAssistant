import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.system import router as system_router
from routes.data import router as data_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc thay "*" bằng frontend URL, ví dụ: ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (POST, GET, OPTIONS, ...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

app.include_router(auth_router, prefix = '/auth')
app.include_router(system_router, prefix='/system')
app.include_router(data_router,prefix='/data')

if __name__ == '__main__':
    import uvicorn
    CustomLogger().get_logger().info("App: __main__")
    uvicorn.run(app, host='127.0.0.1', port=8000)