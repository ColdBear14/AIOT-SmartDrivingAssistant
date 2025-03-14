from fastapi import FastAPI
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix = '/auth')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)