import sys
import time
import serial.tools.list_ports
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["led","pump"]
AIO_USERNAME = "NopeHy14"
AIO_KEY = "aio_GiIc74cdAMPt214e6umJWC5MHNnS"

def connect(client):
    print("Successfully connected to Adafruit IO")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

def subcribe(client, userdata, mid, granted_qos):
    print("Successfully subscribed to Adafruit IO")

def disconnect(client):
    print("Successfully disconnected from Adafruit IO")
    sys.exit(1)

def message(client, feed_id, payload):
    print("Received data from Adafruit IO: " + payload)
    ser.write((str(payload) + "#").encode())

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

if getPort()!= "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    print(ser)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connect
client.on_disconnect = disconnect
client.on_message = message
client.on_subscribe = subcribe
client.connect()
client.loop_background()

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        client.publish("temp", splitData[1])
    elif  splitData[0] == "HUMID":
        client.publish("humidity", splitData[1])
    elif  splitData[0] == "LUX":
        client.publish("bright", splitData[1])
    elif  splitData[0] == "DIS":
        client.publish("distance", splitData[1])

mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    readSerial()
    time.sleep(5)
