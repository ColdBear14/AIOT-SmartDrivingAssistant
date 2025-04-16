import asyncio
import os
import uuid
import httpx

from models.request import IoTDataResponse
from utils.custom_logger import CustomLogger

from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect

class IOTService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IOTService, cls).__new__(cls)
            cls._instance._init_instance()
        return cls._instance
    
    def _init_instance(self):
        self.connected_iot_systems: Dict[str, tuple[WebSocket, str]] = {} # device_id -> [websocket, system_state]
        self.pending_commands: Dict[str, Dict[str, asyncio.Event]] = {}  # device_id -> [command_id: Event]
        self.command_responses: Dict[str, Dict[str, any]] = {}  # device_id -> [command_id: response]

    async def _add_connected_iot_system(self, device_id: str, websocket: WebSocket):
        if device_id not in self.connected_iot_systems:
            await websocket.accept()
            self.connected_iot_systems[device_id] = [websocket, "established"]
            self.pending_commands[device_id] = {}
            self.command_responses[device_id] = {}

            CustomLogger().get_logger().info(f"Successfully connect to device \"{device_id}\"")

        else:
            await websocket.close(code=1008, reason="Device already connected")

            CustomLogger().get_logger().warning(f"Device \"{device_id}\" is already connected")

    async def _establish_connection(self, device_id: str, websocket: WebSocket):
        await self._add_connected_iot_system(device_id, websocket)

        try:
            while True:
                data = await websocket.receive_json()
                try:
                    iot_data = IoTDataResponse(**data)
                    if iot_data.device_id != device_id:
                        CustomLogger().get_logger().error(f"Device ID mismatch: {iot_data.device_id}")
                        await websocket.send_json({"error": "Device ID mismatch"})
                        continue
                    
                    if "command_id" in data and "status" in data:
                        command_id = data["command_id"]
                        if device_id in self.pending_commands and command_id in self.pending_commands[device_id]:
                            # Store response and signal Event
                            self.command_responses[device_id][command_id] = data
                            self.pending_commands[device_id][command_id].set()

                            CustomLogger().get_logger().info(f"Receive response for command \"{command_id}\" from device \"{device_id}\": {data}")

                except Exception as e:
                    CustomLogger().get_logger().error(f"Invalid data from device \"{device_id}\": {e}")
                    await websocket.send_json({"error": "Invalid data"})

        except WebSocketDisconnect:
            CustomLogger().get_logger().info(f"Device \"{device_id}\" disconnected")
            del self.connected_iot_systems[device_id]

        except Exception as e:
            CustomLogger().get_logger().error(f"Websocket error with device \"{device_id}\": {e}")

        finally:
            if device_id in self.connected_iot_systems:
                del self.connected_iot_systems[device_id]

    def _cleanup_device(self, device_id: str):
        """Clean up device state on disconnect."""
        if device_id in self.connected_iot_systems:
            del self.connected_iot_systems[device_id]

        if device_id in self.pending_commands:
            for event in self.pending_commands[device_id].values():
                event.set()

            del self.pending_commands[device_id]
            
        if device_id in self.command_responses:
            del self.command_responses[device_id]

    async def _control_iot_system(self, device_id: str, target: str, command: str):
        if device_id not in self.connected_iot_systems:
            CustomLogger().get_logger().error(f"Device \"{device_id}\" is not connected")
            raise Exception("Device not connected")

        try:
            command_id = str(uuid.uuid4())
            data = {
                "command": {
                    "target": target,
                    "value": command
                },
                "command_id": command_id
            }

            self.pending_commands[device_id][command_id] = asyncio.Event()

            websocket = self.connected_iot_systems[device_id][0]
            await websocket.send_json(data)
            CustomLogger().get_logger().info(f"Sent command \"{command}\" to device \"{device_id}\" with command_id \"{command_id}\"")

            try:
                await asyncio.wait_for(self.pending_commands[device_id][command_id].wait(), timeout=5.0)

            except asyncio.TimeoutError:
                CustomLogger().get_logger().error(f"Timeout waiting for response from device \"{device_id}\"")
                self._cleanup_command(device_id, command_id)
                return False

            if command_id in self.command_responses[device_id]:
                response = self.command_responses[device_id][command_id]
                self._cleanup_command(device_id, command_id)

            # TODO: Handle response
                if response.get("status") == "success":
                    CustomLogger().get_logger().info(f"Device \"{device_id}\" confirmed command \"{command_id}\"")
                    return True
                
                else:
                    CustomLogger().get_logger().error(f"Device \"{device_id}\" response FAIL for command \"{command_id}\": {response}")
                    return False
                
            else:
                CustomLogger().get_logger().error(f"No response received for command \"{command_id}\"")
                return False

        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to control system {device_id}: {e}")
            self._cleanup_command(device_id, command_id)
            return False
    
    def _cleanup_command(self, device_id: str, command_id: str):
        """Clean up command state."""
        if device_id in self.pending_commands and command_id in self.pending_commands[device_id]:
            del self.pending_commands[device_id][command_id]

        if device_id in self.command_responses and command_id in self.command_responses[device_id]:
            del self.command_responses[device_id][command_id]