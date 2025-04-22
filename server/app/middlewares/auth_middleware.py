from utils.custom_logger import CustomLogger

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from datetime import datetime, timedelta

from services.auth_service import AuthService
from services.user_service import UserService

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.whitelist = ["/auth/register", "/auth/login"]
        super().__init__(app)
        CustomLogger()._get_logger().info("Initialized AuthMiddleware")

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for whitelisted paths
        if request.url.path in self.whitelist:
            CustomLogger()._get_logger().info(f"AuthMiddleware: Skip authentication for request \"{request.url.path}\"")
            return await call_next(request)
        
        elif request.method == "OPTIONS":
            CustomLogger()._get_logger().info(f"AuthMiddleware: Accept preflight for request \"{request.url.path}\"")
            return await call_next(request)

        # Check for session token in cookies
        session_token = request.cookies.get("session_token")
        if not session_token:
            CustomLogger()._get_logger().info("AuthMiddleware: Missing session token for request \"{request.url.path}\"")
            return JSONResponse(
                content={"detail": "Unauthorized: Missing session token"},
                status_code=401
            )

        user = UserService()._get_user_info_by_session_token(session_token)
        
        if not user:
            CustomLogger()._get_logger().info("AuthMiddleware: Invalid or expired session token for request \"{request.url.path}\"")
            return JSONResponse(
                content={"detail": "Unauthorized: Invalid or expired session token"},
                status_code=401
            )

        CustomLogger()._get_logger().info(f"AuthMiddleware: User info: {user['username']} - {str(user['_id'])}")

        user_id = user["_id"]
        expiration_time = user["session_expiration"]

        request.state.user_id = str(user_id)

        # Check session expiration
        if expiration_time.timestamp() - datetime.now().timestamp() < timedelta(minutes=10).total_seconds():
            CustomLogger()._get_logger().info(f"AuthMiddleware: Refreshing session for user {user_id}")
            new_session_token = AuthService()._create_session(user_id)

            if not new_session_token:
                return JSONResponse(
                    content={"detail": "Server Error: Unable to refresh session"},
                    status_code=500
                )
            
            response = await call_next(request)
            response = AuthService()._add_session_to_cookie(response, new_session_token)
            return response

        return await call_next(request)