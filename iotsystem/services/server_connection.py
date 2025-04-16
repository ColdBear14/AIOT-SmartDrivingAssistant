from helpers.custom_logger import CustomLogger

import os
from dotenv import load_dotenv
import websockets
import asyncio
import json

from services.iot import IOTSystem

class ServerConnection:
    _instance = None

    def __new__(cls, uid: str = None):
        if not cls._instance:
            cls._instance = super(ServerConnection, cls).__new__(cls)
            cls._instance._init_instance(uid)
        return cls._instance
    
    def _init_instance(self, uid: str = None):
        load_dotenv()

        self.uid = uid

        if uid == None:
            self.connection_url = None
        else:
            server_url = os.getenv('SERVER_URL')
            # Convert http:// or https:// to ws:// or wss:// respectively
            if server_url.startswith('https://'):
                ws_url = 'wss://' + server_url[8:]
            else:
                ws_url = 'ws://' + server_url[7:] if server_url.startswith('http://') else 'ws://' + server_url
            self.connection_url = f"{ws_url}/iot/ws/{uid}"

    def _delete_server_connection(self):
        pass

    async def _connect_to_server(self):
        if self.uid == None:
            raise Exception("User ID is required to connect to the server.")

        max_retries = 5
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                async with websockets.connect(self.connection_url) as websocket:
                    CustomLogger().get_logger().info(f"Connected to server as {self.uid}")

                    # Run send and receive tasks concurrently
                    await asyncio.gather(
                        self._receive_server_commands(websocket),
                        self._track_device_status(websocket)
                    )

            except (websockets.exceptions.WebSocketException, ConnectionError) as e:
                CustomLogger().get_logger().error(f"Connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    CustomLogger().get_logger().error("Max retries reached. Giving up.")
                    break

            except Exception as e:
                CustomLogger().get_logger().error(f"Unexpected error: {e}")
                break

    async def _receive_server_commands(self, websocket):
        try:
            async for message in websocket:
                data = json.loads(message)
                CustomLogger().get_logger().info(f"Received command: {data}")

                if not "command" in data or not "command_id" in data:
                    continue

                command = data["command"]
                command_id = data["command_id"]

                if command["target"] == "system":
                    if command["value"] == "on":
                        try:
                            await IOTSystem().start_system(self.uid)
                            
                            CustomLogger().get_logger().info(f"Started system {self.uid}")
                            await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "success"}))
                        
                        except Exception as e:
                            CustomLogger().get_logger().error(f"Failed to start system: {e}")
                            await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "fail"}))
                            continue

                    elif command["value"] == "off":
                        try:
                            await IOTSystem().stop_system(self.uid)

                            CustomLogger().get_logger().info(f"Stopped system {self.uid}")
                            await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "success"}))

                        except Exception as e:
                            CustomLogger().get_logger().error(f"Failed to stop system: {e}")
                            await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "fail"}))
                            continue
                        
                elif "service" in command["target"]:
                    try:
                        await IOTSystem().control_service(command["target"], command["value"])

                        CustomLogger().get_logger().info(f"Controlled service {command['target']} with value {command['value']}")
                        await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "success"}))

                    except Exception as e:
                        CustomLogger().get_logger().error(f"Failed to control service: {e}")
                        await websocket.send(json.dumps({"device_id": self.uid, "command_id": command_id, "status": "fail"}))
                        continue

        except websockets.exceptions.ConnectionClosed:
            CustomLogger().get_logger().warning("Disconnected")
 
        except Exception as e:
            CustomLogger().get_logger().error(f"Error receiving commands: {e}")

    async def _track_device_status(self, websocket):
        pass

    async def _send_data_to_server(self, websocket, data: dict = None):
        pass
