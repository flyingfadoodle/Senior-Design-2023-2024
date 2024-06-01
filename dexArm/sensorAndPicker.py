import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys

def initializePressureFlipperArduino(wait=True):
    global pressure_flipperArduinoSerial
    port = "COM24"
    baud = 115200
    pressure_flipperArduinoSerial = serial.Serial(port, baud, timeout = 0.1)
    global serial_line 
    serial_line = pressure_flipperArduinoSerial.readline()
    if wait == True:
        time.sleep(3)


def detect():
    message = "$M\n"
    pressure_flipperArduinoSerial.write((bytes(message, 'utf-8')))
    # Wait until flipper station sequence finished
    while True:
        messageIncoming = pressure_flipperArduinoSerial.readline()
        print(serial_line) # for debug
        if(len(messageIncoming) > 0):
            print(messageIncoming)
            if(chr(messageIncoming[1]) == 'D'):
                break;

def FlipperStationGo():
    message = "$F\n"
    pressure_flipperArduinoSerial.write((bytes(message, 'utf-8')))
    # Wait until flipper station sequence finished
    while True:
        messageIncoming = pressure_flipperArduinoSerial.readline()
        print(serial_line) # for debug
        if(len(messageIncoming) > 0):
            print(messageIncoming)
            if(chr(messageIncoming[1]) == 'D'):
                break;

initializePressureFlipperArduino()
detect()

dexarm1 = Dexarm(port="COM19")
dexarm1.go_home()#Goes to robot home position

