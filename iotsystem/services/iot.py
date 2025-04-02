from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger

import asyncio
import serial_asyncio
from Adafruit_IO import MQTTClient
from services.database import Database
import serial.tools.list_ports

class IOTSystem:
    _instance = None

    __AIO_FEED_ID = ['led', 'fan']

    def __new__(cls, config=None):
        if not cls._instance:
            cls._instance = super(IOTSystem, cls).__new__(cls)
            cls._instance._init_iot_system(config)
        return cls._instance

    def _init_iot_system(self, config=None):
        CustomLogger().get_logger().info("IOT System initialized.")
        
        # Auto load config from .env file if not provided 
        if config is None or not config.contains("aio_user") or not config.contains("aio_key"):
            from dotenv import load_dotenv
            import os

            load_dotenv()
            config = {
                "aio_user": os.getenv("AIO_USER_NAME"),
                "aio_key": os.getenv("AIO_KEY")
            }
            CustomLogger().get_logger().info("IOT System's config: " + str(config))

        self.__AIO_USERNAME = config["aio_user"]
        self.__AIO_KEY = config["aio_key"]

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

        self.client = MQTTClient(self.__AIO_USERNAME, self.__AIO_KEY)
        self.client.on_connect = self.connect
        self.client.on_disconnect = self.disconnect
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

    async def connect_serial(self, port):
        """Async function to connect to serial device."""
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=port, baudrate=115200)
            # print(f"Connected to serial: {port}")
            CustomLogger().get_logger().info(f"Connected to serial: {port}")
        except Exception as e:
            # print(f"Failed to connect to serial: {e}")
            CustomLogger().get_logger().exception(f"Failed to connect to serial: {e}")

    def connect(self, client):
        # print("Connected to Adafruit IO")
        CustomLogger().get_logger().info("Connected to Adafruit IO")
        for feed in IOTSystem.__AIO_FEED_ID:
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        # print("Subscribed to Adafruit IO")
        CustomLogger().get_logger().info("Subscribed to Adafruit IO")

    def disconnect(self, client):
        # print("Disconnected. Reconnecting...")
        CustomLogger().get_logger().info("Disconnected. Reconnecting...")
        asyncio.create_task(self.reconnect())

    async def reconnect(self):
        while True:
            try:
                self.client.connect()
                self.client.loop_background()
                # print("Reconnected!")
                CustomLogger().get_logger().info("Reconnected!")
                break
            except Exception as e:
                # print(f"Reconnect failed: {e}, retrying in 5 sec...")
                CustomLogger().get_logger().exception(f"Reconnect failed: {e}, retrying in 5 sec...")
                await asyncio.sleep(5)

    def message(self, client, feed_id, payload):
        CustomLogger().get_logger().info(f"Received: {payload}")
        if self.writer:
            self.writer.write(f"!{feed_id}:{payload}#".encode())

    async def sendSerial(self, uid):
        """Sends data to the serial device."""
        if self.writer:
                self.writer.write(f"!:#".encode())
                # print(f"Sent: {data}")
                CustomLogger().get_logger().info(f"Sent: ")


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
        # print(f"Processed: {sensor_type} = {value}")
        CustomLogger().get_logger().info(f"Processed: {sensor_type} = {value}")

        sensor_map = {
            "temp": "temperature",
            "humid": "humidity",
            "lux": "bright",
            "dis": "distance"
        }
        if sensor_type in sensor_map:
            self.client.publish(sensor_map[sensor_type], value)

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

    async def start_system(self, uid):
        if not self.running:
            self.running = True
            asyncio.create_task(self.readSerial(uid))
            # print("IOT System started.")
            CustomLogger().get_logger().info("IOT System started.")
        else:
            # print("System already running.")
            CustomLogger().get_logger().warning("System already running.")

    def stop_system(self):
        self.running = False
        # print("IOT System stopped.")
        CustomLogger().get_logger().info("IOT System stopped.")

if __name__ == "__main__":
    CustomLogger().get_logger().info("IOT System: __main__")
    iotsystem = IOTSystem()._instance
    asyncio.run(iotsystem.start_system('123'))
