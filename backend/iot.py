import sys
import time
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from database import Database
from config import config
import threading

class IOTSystem:
    AIO_FEED_ID = ['led', 'pump']
    AIO_USERNAME = config.aio_user
    AIO_KEY = config.aio_key

    def __init__(self):
        self.db = Database()
        self.mess = ""
        self.running = False
        
        port = IOTSystem.getPort()
        if port != "None":
            self.ser = serial.Serial(port=port, baudrate=115200)
            print(self.ser)
        else:
            self.ser = None  # Handle case where no port is available

        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connect
        self.client.on_disconnect = self.disconnect
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

    def connect(self, client):
        print("Successfully connected to Adafruit IO")
        for feed in IOTSystem.AIO_FEED_ID:
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Successfully subscribed to Adafruit IO")

    def disconnect(self, client):
        print("Successfully disconnected from Adafruit IO")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Received data from Adafruit IO:", payload)
        if self.ser:
            self.ser.write((str(payload) + "#").encode())

    @staticmethod
    def getPort():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB-SERIAL" in str(port):
                return str(port).split(" ")[0]
        return "None"

    def readSerial(self):
        if not self.ser:
            print("No serial connection available.")
            return
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            self.mess += self.ser.read(bytesToRead).decode("UTF-8")
            while "!" in self.mess and "#" in self.mess:
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.processData(self.mess[start:end + 1])
                self.mess = self.mess[end + 1:] if end < len(self.mess) else ""

    def processData(self, data):
        data = data.replace("!", "").replace("#", "")
        splitData = data.split(":")
        if len(splitData) < 2:
            return  # Prevent errors on malformed data

        sensor_type = splitData[0]
        value = splitData[1]
        print("Processed data:", sensor_type, value)

        sensor_map = {
            "TEMP": "temp",
            "HUMID": "humidity",
            "LUX": "bright",
            "DIS": "distance"
        }
        if sensor_type in sensor_map:
            self.client.publish(sensor_map[sensor_type], value)

        try:
            doc = {'sensor_type': sensor_type.lower(), 'value': float(value)}
            self.db.push_to_db('environment_sensor', doc)
        except ValueError:
            print(f"Invalid data format for {sensor_type}: {value}")
    def _run_system(self):
        while self.running:
            self.readSerial()
            time.sleep(5)
            
    def start_system(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_system)
            self.thread.start()
            print("System started in background")
        print("System is already online")
        
    def stop_system(self):
        if self.running:
            self.running = False
            print("System stopped.")
        else:
            print("System is offline")
    
if __name__ == "__main__":
    iotsystem = IOTSystem()
    count = 1
    while True:
        if count == 1:
            iotsystem.start_system()
        count = 0