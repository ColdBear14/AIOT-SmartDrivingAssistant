import sys
import time
import serial
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from database import Database
from config import config
import threading
from datetime import datetime

class IOTSystem(threading.Thread):
    AIO_FEED_ID = ['led', 'fan']
    AIO_USERNAME = config.aio_user
    AIO_KEY = config.aio_key

    def __init__(self):
        super().__init__(daemon=True)
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
    def client_connect(self):
        self.client.loop_forever()
    def connect(self, client):
        print("Successfully connected to Adafruit IO")
        for feed in IOTSystem.AIO_FEED_ID:
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Successfully subscribed to Adafruit IO")

    def disconnect(self, client):
        print("Disconnected from Adafruit IO. Attempting to reconnect...")
        while True:  # Keep trying to reconnect
            try:
                self.client.connect()
                self.client.loop_background()
                print("Reconnected to Adafruit IO!")
                break  # Exit loop if successful
            except Exception as e:
                print(f"Reconnect failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def message(self, client, feed_id, payload):
        print("Received data from Adafruit IO:", payload)
        if self.ser:
            self.ser.write("!" + str(feed_id) + ":" + (str(payload) + "#").encode())

    @staticmethod
    def getPort():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB-SERIAL" in str(port):
                return str(port).split(" ")[0]
        return "None"

    def readSerial(self,uid):
        if not self.ser:
            print("No serial connection available.")
            return
        bytesToRead = self.ser.inWaiting()
        if bytesToRead > 0:
            self.mess += self.ser.read(bytesToRead).decode("UTF-8")
            while "!" in self.mess and "#" in self.mess:
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.processData(self.mess[start:end + 1],uid)
                self.mess = self.mess[end + 1:] if end < len(self.mess) else ""

    def processData(self, data,uid):
        data = data.replace("!", "").replace("#", "")
        splitData = data.split(":")
        if len(splitData) < 2:
            return  # Prevent errors on malformed data

        sensor_type = splitData[0].lower()
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
            doc = {
                'timestamp': datetime.now(),
                'metadata':{
                    'sensor_type': sensor_type,
                    'uid': uid
                },
                'val': value
            }
            self.db.insert_collection('environment_sensor', doc)
        except ValueError:
            print(f"Invalid data format for {sensor_type}: {value}")
            
    def run(self):
        while self.running:
            self.readSerial(self.uid)
            time.sleep(1)
    def start_system(self,uid):
        if not self.running:
            self.uid = uid
            self.running = True
            self._run_system(uid)
            print("System started in background")
        else: 
            print("System is already online")
            
    def stop_system(self):
        if self.running:
            self.running = False
            print("System stopped.")
        else:
            print("System is offline")
    
if __name__ == "__main__":
    iotsystem = IOTSystem()
    iotsystem.start_system('123')
    while True:
        time.sleep(1)
        print("Main thread is running...")