import serial
import time


def initializePressureFlipperArduino(wait=True):
    global pressure_flipperArduinoSerial
    port = "COM25"
    baud = 115200
    pressure_flipperArduinoSerial = serial.Serial(port, baud, timeout = 0.1)
    global serial_line 
    serial_line = pressure_flipperArduinoSerial.readline()
    if wait == True:
        time.sleep(3)

def PressureStationGo():
    message = "$P\n"
    pressure_flipperArduinoSerial.write((bytes(message, 'utf-8')))
    # Wait until pressure station sequence finished
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
