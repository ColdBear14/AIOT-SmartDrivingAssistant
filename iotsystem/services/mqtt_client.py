import paho.mqtt.client as mqtt
import json
from helpers.custom_logger import CustomLogger
import asyncio

class MQTTClient:
    _instance = None
    BROKER = "broker.hivemq.com"
    PORT = 1883
    CONTROL_TOPIC = "scs/control/{user_id}"  # Topic for control commands

    def __new__(cls, user_id=None):
        if cls._instance is None:
            cls._instance = super(MQTTClient, cls).__new__(cls)
            cls._instance._init_mqtt(user_id)
        return cls._instance

    def _init_mqtt(self, user_id):
        self.user_id = user_id
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.connected = False

        try:
            self.client.connect(self.BROKER, self.PORT, 60)
            self.client.loop_start()
            CustomLogger().get_logger().info(f"Connected to MQTT broker at {self.BROKER}")
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to connect to MQTT broker: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            CustomLogger().get_logger().info("Connected to MQTT broker successfully")
            # Subscribe to control topic for this user
            control_topic = self.CONTROL_TOPIC.format(user_id=self.user_id)
            self.client.subscribe(control_topic)
            CustomLogger().get_logger().info(f"Subscribed to {control_topic}")
        else:
            CustomLogger().get_logger().error(f"Failed to connect to MQTT broker with code: {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            topic_parts = msg.topic.split('/')
            
            if len(topic_parts) != 3:
                return
            
            category, action, user_id = topic_parts
            
            if action == "control" and user_id == self.user_id:
                # Handle control commands
                CustomLogger().get_logger().info(f"Received control command: {payload}")
                asyncio.create_task(self._handle_control_command(payload))
                
        except Exception as e:
            CustomLogger().get_logger().error(f"Error processing MQTT message: {e}")

    async def _handle_control_command(self, command):
        try:
            from services.iot import IOTSystem
            if command.get("command") == "start_system":
                await IOTSystem()._instance.start_system(self.user_id)
            elif command.get("command") == "stop_system":
                await IOTSystem()._instance.stop_system()
            else:
                # Process other control commands
                await IOTSystem()._instance.control_service(
                    command.get("service_type"),
                    command.get("value")
                )
        except Exception as e:
            CustomLogger().get_logger().error(f"Error handling control command: {e}")

    def cleanup(self):
        """Cleanup MQTT client connection"""
        if hasattr(self, 'client'):
            self.client.loop_stop()
            self.client.disconnect()