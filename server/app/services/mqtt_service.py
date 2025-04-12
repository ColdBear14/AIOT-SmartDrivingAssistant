import paho.mqtt.client as mqtt
from utils.custom_logger import CustomLogger
import json

class MQTTService:
    _instance = None
    BROKER = "broker.hivemq.com"
    PORT = 1883
    CONTROL_TOPIC = "scs/control/{user_id}"  # Topic for control commands

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQTTService, cls).__new__(cls)
            cls._instance._init_mqtt()
        return cls._instance

    def _init_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        
        try:
            self.client.connect(self.BROKER, self.PORT, 60)
            self.client.loop_start()
            CustomLogger().get_logger().info(f"Connected to MQTT broker at {self.BROKER}")
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to connect to MQTT broker: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            CustomLogger().get_logger().info("Connected to MQTT broker successfully")
        else:
            CustomLogger().get_logger().error(f"Failed to connect to MQTT broker with code: {rc}")

    def send_control_command(self, user_id: str, command: dict):
        """Send control command to specific IoT system"""
        topic = self.CONTROL_TOPIC.format(user_id=user_id)
        try:
            self.client.publish(topic, json.dumps(command))
            CustomLogger().get_logger().info(f"Sent control command to {topic}: {command}")
            return True
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to send control command: {e}")
            return False

    def cleanup(self):
        """Cleanup MQTT client connection"""
        if hasattr(self, 'client'):
            self.client.loop_stop()
            self.client.disconnect()