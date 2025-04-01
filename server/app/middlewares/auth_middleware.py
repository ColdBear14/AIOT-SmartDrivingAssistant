# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.custom_logger import CustomLogger

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from datetime import datetime, timedelta

from services.auth_service import AuthService #, redis_client
from services.user_service import UserService

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.whitelist = ["/auth/register", "/auth/login"]
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for whitelisted paths
        if request.url.path in self.whitelist:
            CustomLogger().get_logger().info(f"AuthMiddleware: Skip authentication for {request.url.path}")
            return await call_next(request)
        
        elif request.method == "OPTIONS":
            CustomLogger().get_logger().info(f"AuthMiddleware: Preflight request for {request.method}-{request.url.path}")
            return await call_next(request)

        # Check for session token in cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            return JSONResponse({"detail": "Unauthorized: Missing session token"}, status_code=401)

    # Validate session in Redis
        # session_data = redis_client.hgetall(session_id)
        # if not session_data:
        #     return JSONResponse({"detail": "Unauthorized: Invalid or expired session token"}, status_code=401)

        # user_id = session_data.get("user_id")
        # expiration_time = session_data.get("expiration_time")

        user = UserService()._get_user_info_by_session_id(session_id)
        
        if not user:
            return JSONResponse(
                content={"detail": "Unauthorized: Invalid or expired session token"},
                status_code=401
            )

        CustomLogger().get_logger().info(f"AuthMiddleware: User info: {user['username']} - {str(user['_id'])}")

        user_id = user["_id"]
        expiration_time = user["session_expiration"]

        request.state.user_id = str(user_id)

        # Check session expiration
        if expiration_time.timestamp() - datetime.now().timestamp() < timedelta(minutes=10).total_seconds():
            CustomLogger().get_logger().info(f"AuthMiddleware: Refreshing session for user {user_id}")
            new_session_id = AuthService()._create_session(user_id)

            if not new_session_id:
                return JSONResponse(
                    content={"detail": "Server Error: Unable to refresh session"},
                    status_code=500
                )
            
            response = await call_next(request)
            response = AuthService()._add_cookie_session(response, new_session_id)
            return response

        return await call_next(request)