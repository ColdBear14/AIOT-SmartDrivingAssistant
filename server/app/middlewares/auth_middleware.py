from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from services.auth_service import redis_client, AuthService
from datetime import datetime, timedelta

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.whitelist = ["/user/register", "/user/login"]
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for whitelisted paths
        if request.url.path in self.whitelist:
            return await call_next(request)

        # Check for session token in cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            return JSONResponse({"detail": "Unauthorized: Missing session token"}, status_code=401)

        # Validate session in Redis
        session_data = redis_client.hgetall(session_id)
        if not session_data:
            return JSONResponse({"detail": "Unauthorized: Invalid or expired session token"}, status_code=401)
        
        user_id = session_data.get("user_id")
        expiration_time = session_data.get("expiration_time")

        # Check session expiration
        if expiration_time - datetime.now().timestamp() < timedelta(minutes=10):
            new_session_id = self._refresh_session(user_id, session_id)
            if not new_session_id:
                return JSONResponse({"detail": "Server Error: Unable to refresh session"}, status_code=500)
            
            response = await call_next(request)
            response.set_cookie(
                key="session_id",
                value=new_session_id,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=3600
            )
            return response


        # Attach user info to the request for further use
        request.state.user_id = user_id
        return await call_next(request)
    
    def _refresh_session(self, user_id: str = None, session_id: str = None) -> str:
        if not user_id or not session_id:
            raise Exception("User ID and session ID are required")
        
        redis_client.delete(session_id)
        
        new_session_id = AuthService()._create_session(user_id)
        return new_session_id