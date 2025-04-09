from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger

import asyncio
import serial_asyncio
from services.database import Database
import serial.tools.list_ports

from services.webcam import VideoCam

WAIT_TIME = 5.0
EAR_THRESHOLD = 0.25 

class IOTSystem:
    _instance = None

    FIELD_UID = "uid"
    FIELD_DEVICE_TYPE = "device_type"
    FIELD_TIMESTAMP = "timestamp"
    FIELD_VAL = "val"

    def __new__(cls, config=None):
        if not cls._instance:
            cls._instance = super(IOTSystem, cls).__new__(cls)
            cls._instance._init_iot_system(config)
        return cls._instance

    def _init_iot_system(self, config=None):
        CustomLogger().get_logger().info("IOT System initialized.")

        self.db = Database()._instance
        self.running = False
        self.reader = None
        self.writer = None
        
        port = self.getPort()
        if port != "None":
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.connect_serial(port)) 
            except RuntimeError:
                asyncio.run(self.connect_serial(port))
        else:
            # print("No serial device found.")
            CustomLogger().get_logger().info("No serial device found.")

        
        self.videocam = VideoCam()

    async def connect_serial(self, port):
        """Async function to connect to serial device."""
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=port, baudrate=115200)
            # print(f"Connected to serial: {port}")
            CustomLogger().get_logger().info(f"Connected to serial: {port}")
        except Exception as e:
            # print(f"Failed to connect to serial: {e}")
            CustomLogger().get_logger().exception(f"Failed to connect to serial: {e}")

    def recieveData(self, uid, data):
        device_name = data.get("name")
        device_value = data.get("max")
        try:
            doc = {
                'uid': str(uid),
                'device_type': str(device_name).lower(), 
                'value': float(device_value)
            }
        except Exception as e:
            return None
        # Add the document to the database
        Database()._instance._add_doc_with_timestamp('device_control', doc)

    async def sendSerial(self, uid):
        """Sends data to the serial device."""
        while self.running:
            try:
                # Set up the change stream to watch for updates
                with Database()._instance.get_device_collection().watch() as stream:
                    for change in stream:
                        # Check if the change is relevant to the given UID
                        if change['operationType'] == 'insert':
                            doc = change['fullDocument']
                            doc["_id"] = str(doc["_id"])
                            CustomLogger().get_logger().info(f"Data retrieved: {doc}")

                            feed = doc["device_type"]
                            payload = doc["value"]

                            message = f"!{feed}:{payload}#"
                            CustomLogger().get_logger().info(f"Sending data: {message}")

                            if self.writer:
                                self.writer.write(message.encode())
                                CustomLogger().get_logger().info(f"Sent: {message}")

            except asyncio.CancelledError:
                CustomLogger().get_logger().info("sendSerial task was cancelled.")
                break
            except Exception as e:
                CustomLogger().get_logger().exception(f"Error watching database changes: {e}")

            
    @staticmethod
    def getPort():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB-SERIAL" in str(port):
                return str(port).split(" ")[0]
        return "None"

    async def readSerial(self, uid):
        """Reads and processes serial data asynchronously."""
        if not self.reader:
            # print("No serial connection available.")
            CustomLogger().get_logger().warning("No serial connection available.")
            return
        while self.running:
            try:
                data = await self.reader.readuntil(b"#")
                data = data.decode("UTF-8").replace("#", "").replace("!", "")
                CustomLogger().get_logger().info(f"Received data: {data}")
                await self.processData(data, str(uid))
            except Exception as e:
                # print(f"Serial read error: {e}")
                CustomLogger().get_logger().exception(f"Serial read error: {e}")
            await asyncio.sleep(1)

    async def processData(self, data, uid):
        """Processes incoming serial data and stores it in DB."""
        CustomLogger().get_logger().info(f"Processing data: {data}")
        splitData = data.split(":")
        if len(splitData) < 2:
            return
        sensor_type, value = splitData[0], splitData[1]
        CustomLogger().get_logger().info(f"Processed: {sensor_type} = {value}")

        sensor_map = {
            "temp": "temperature",
            "humid": "humidity",
            "lux": "bright",
            "dis": "distance"
        }

        try:
            doc: dict = {
                'uid': str(uid),
                'sensor_type': sensor_type.lower(), 
                'value': float(value)
            }

            Database()._instance._add_doc_with_timestamp('environment_sensor', doc)
        except ValueError:
            # print(f"Invalid data format: {sensor_type} -> {value}")
            CustomLogger().get_logger().exception(f"Invalid data format: {sensor_type} -> {value}")

    async def start_webcam(self,uid):
        # call to database for user preferences
        try:
            doc = await self.db.get_user_doc_by_id(uid)
            if doc is None:
                thresholds = {'ear_threshold': EAR_THRESHOLD, 'wait_time': WAIT_TIME, 'show_window': True}
                
            else:
                thresholds = doc.get('camera', {'ear_threshold': EAR_THRESHOLD, 'wait_time': WAIT_TIME, 'show_window': True})
                
        except Exception as e:
            CustomLogger().get_logger().exception(f"Error getting user {uid} from database: {e}")
            thresholds = {'ear_threshold': EAR_THRESHOLD, 'wait_time': WAIT_TIME, 'show_window': True}
        
        if self.videocam:
            await self.videocam.start_webcam(thresholds)
            
        else:
            CustomLogger().get_logger().warning("Webcam not initialized.")
            
    async def start_system(self, uid):
        if not self.running:
            self.running = True
            asyncio.create_task(self.readSerial(uid))
            asyncio.create_task(self.sendSerial(uid))
            # CustomLogger().get_logger().info("Sensor System started.")
            
            asyncio.create_task(self.start_webcam(uid))
            CustomLogger().get_logger().info("Webcam System started.")
        else:
            # print("System already running.")
            CustomLogger().get_logger().warning("System already running.")

    async def stop_system(self):
        self.running = False
        self.videocam.stop()
        # print("IOT System stopped.")
        CustomLogger().get_logger().info("IOT System stopped.")

if __name__ == "__main__":
    import time
    CustomLogger().get_logger().info("IOT System: __main__")
    iotsystem = IOTSystem()._instance
    asyncio.run(iotsystem.start_system('123'))
    
    
    time.sleep(20)
    
    iotsystem.stop_system()
