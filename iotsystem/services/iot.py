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

FIELD_ACCESS = {
    'air_cond_service': ('humid','temp'),
    'dist_service': 'dis',
    'headlight_service': 'lux',
    'drowsiness_service': 'camera',
    'drowsiness_threshold': 'wait_time',
}

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
        
        self.states = {
            'humid': True,
            'temp': True,
            'headlight': True,
            'camera': True,
            'dis': True
        }
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
        if self.states[sensor_type]:
            CustomLogger().get_logger().info(f"Processed: {sensor_type} = {value}")
            if self.states[sensor_type]:
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
        thresholds = {'show_window': True}
        if self.videocam:
            await self.videocam.start_webcam(thresholds)
            last_alarm_state = None
            while self.videocam.running:
                await asyncio.sleep(0.1)
                if hasattr(self.videocam,'last_frame'):
                    _,play_alarm = self.videocam.last_frame
                    if play_alarm != last_alarm_state:
                        value = '1' if play_alarm else '0'
                        self.db._add_doc_with_timestamp('device_control',{'uid': str(uid), 'device_type': 'alarm','value': value})
                        last_alarm_state = play_alarm                    
            
        else:
            CustomLogger().get_logger().warning("Webcam not initialized.")
    async def _resolve_service(self, uid):
        try:
            services = Database()._instance.get_services_doc_by_id(uid,False)
            if services is None:
                CustomLogger().get_logger().info("No services found for this user.")
                return None
            
            for service in services:
                convert_service = FIELD_ACCESS.get(service,None)
                if convert_service is not None:
                    raise ValueError(f"Invalid service type: {service}")
                if isinstance(convert_service, tuple):
                    for convert in convert_service:
                        self.states[convert] = service['value']
                        
                elif convert_service in ['lux','dis','camera']:
                    self.states[convert_service] = service['value']
                else:
                    self.videocam.set_time_threshold(service['value'])
            
        except Exception as e:
            CustomLogger().get_logger().exception(f"Error resolving service: {e}")
            return None
        
    async def start_system(self, uid):
        if not self.running:
            self.running = True
            
            await self._resolve_service(uid)
            
            # asyncio.create_task(self.readSerial(uid))
            # asyncio.create_task(self.sendSerial(uid))
            # CustomLogger().get_logger().info("Sensor System started.")
            if self.states['camera']:
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
    async def stop_camera(self,uid):
        if self.videocam:
            self.videocam.stop()
            CustomLogger().get_logger().info("Webcam System stopped.")
        else:
            CustomLogger().get_logger().warning("Webcam not initialized.")
    async def start_camera(self,uid):
        asyncio.create_task(self.start_webcam(uid))
        CustomLogger().get_logger().info("Webcam System started.")
    async def control_service(self,uid:str, service_type: str, value: any = None):
        """Controls a service state (on/off) and sends appropriate commands to YOLO"""
        # if not self.writer:
        #     CustomLogger().get_logger().warning("No serial connection available")
        #     return False
        
# TODO: Create command to control a specific service based on service_type and value
    # Example command: !air_cond:1#
        if service_type.startswith("air_cond"):
            convert_type = ["humid","temp"], "fan"
        elif service_type.startswith("headlight"):
            convert_type = ["lux"],None
        elif service_type.startswith("drowsiness"):
            convert_type = ["camera"],None
        elif service_type.startswith("dist"):
            convert_type = ["dis"],None
        else:
            CustomLogger().get_logger().warning(f"Unknown service type: {service_type}")
            return False

        write_type = service_type
        
        if isinstance(value, str):
            # Handle on/off states
            for cvt in convert_type[0]:
                self.states[cvt] = value.lower() == "on"
            
        elif value is not None:
            # Handle numeric values for thresholds, temperature, etc.
            if service_type.startswith('drowsiness'):
                print(self.videocam)
                await self.videocam.set_time_threshold(value)
                write_type = 'drowsiness_threshold'
            elif convert_type[1] is not None:
                command = f'{convert_type[1]}:{value}#'
                write_type = 'air_cond_temp'
            else:
                command = f'{convert_type[0][0]}:{value}#'
                write_type = 'headlight_brightness'
        else:
            command = f'{convert_type[0][0]}:1#'
            write_type = 'air_cond_temp' if convert_type[0][0] == 'temp' else 'headlight_brightness'
        
    # End example!
        try :
            if 'command' in locals():
                self.writer.write(command.encode())
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to send service command: {e}")
            raise e

        session = Database()._instance.client.start_session()
        try:
            with session.start_transaction():
                try:
                    await self.update_service_status(
                        uid=uid,
                        service=write_type,
                        status=value if value is not None else 1
                    )
                except Exception as e:
                    CustomLogger().get_logger().error(f"Failed to update service status: {e}")
                    raise e
                # write action history to database
                try:
                    await self.write_action_history(
                        uid=uid,
                        service_type=write_type,
                        value=value if value is not None else 1
                    )
                except Exception as e:
                    CustomLogger().get_logger().error(f"Failed to write action history: {e}")
                    raise e
                
        except Exception as e:
            session.abort_transaction()
            CustomLogger().get_logger().error(f"Failed to update service status: {e}")
            raise e

        return True
            
        
    async def write_action_history(self, uid: str = None, service_type: str = None, value: int = None):
        try:
            action = {
                "uid": uid,
                "service_type": service_type,
                "description": f'{service_type} set to {value}'
            }

            Database()._instance._add_doc_with_timestamp('action_history', action)
        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to write action history: {e}")
            raise e
        
    async def update_service_status(self, uid: str = None, service: str = None, status: str = None):
        try:
            result = Database()._instance.get_services_status_collection().find_one(
                {
                    "uid": uid
                }
            )

            if not result:
                # If no document found, create a new one
                await Database()._instance._add_doc_with_timestamp(
                    'services_status',
                    {
                        "uid": uid,
                        service: status
                    }
                )
            else:
                Database()._instance.get_services_status_collection().update_one(
                    {
                        "uid": uid
                    },
                    {
                        "$set": {
                            service: status
                        }
                    }
                )

        except Exception as e:
            CustomLogger().get_logger().error(f"Failed to update service status: {e}")
            raise e

if __name__ == "__main__":
    import time
    CustomLogger().get_logger().info("IOT System: __main__")
    iotsystem = IOTSystem()._instance
    asyncio.run(iotsystem.start_system('123'))
    
    
    time.sleep(20)
    
    iotsystem.stop_system()
