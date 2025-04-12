import os
import httpx
from utils.custom_logger import CustomLogger

class IOTService:
    def _create_init_iot_system_date(self, uid: str = None):
        pass

    def _get_iot_system_connection_detail(self, uid: str = None):
        pass

    def _update_iot_system_connection_detail(self, uid: str = None, connection_detail: dict = None):
        pass
    
    async def _toggle_service(self, uid: str = None, service_type: str = None, value: int = None):
        """
        Send control request to IoT system to control a specific service.
        """
        try:
            iot_server_url = os.getenv("IOT_SERVER_URL")
            iot_server_port = os.getenv("IOT_SERVER_PORT")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{iot_server_url}:{iot_server_port}/service",
                    json={
                        "user_id": uid,
                        "service_type": service_type,
                        "value": value
                    }
                )
                
                CustomLogger().get_logger().info(f"Control service response: {response.status_code}")
                return response.status_code == 200
                
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to control service: {e}")
            return False
    def _send_slider_data(self, uid: str = None, value: str = None):
        """
        Send slider data to iotsystem.
        """        
        try:
            # Send slider data to IOTSystem
            IOTSystem().recieveData(uid, value)
        except Exception as e:
            return None