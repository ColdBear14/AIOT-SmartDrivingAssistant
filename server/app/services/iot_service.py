import os
import httpx
from utils.custom_logger import CustomLogger
from services.mqtt_service import MQTTService

from models.mongo_doc import ActionHistoryDocument

class IOTService:
    def __init__(self):
        self.mqtt_service = MQTTService()

    def _create_init_iot_system_date(self, uid: str = None):
        pass

    def _get_iot_system_connection_detail(self, uid: str = None):
        pass

    def _update_iot_system_connection_detail(self, uid: str = None, connection_detail: dict = None):
        pass
    
    async def _control_service(self, uid: str = None, service_type: str = None, value: any = None):
        """
        Send control request to IoT system via MQTT.
        """
        try:
            command = {
                "service_type": service_type,
                "value": value
            }
            
            success = self.mqtt_service.send_control_command(uid, command)
            CustomLogger().get_logger().info(f"Control service response: {success}")
            return success
                
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to control service: {e}")
            return False