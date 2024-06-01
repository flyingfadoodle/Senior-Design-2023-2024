import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import serial
import re

stepMovSize = 10
speedRobot = 6000
railStep = 60
offset = 0
m_value = ""

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

            #line = pressure_flipperArduinoSerial.readline().decode().strip()

            #if line.startswith('b\'$M'):
                #m_value = re.search(r'(\d+)', line)
                #other = m_value.group()
                #offset = int(m_value)
                #print("hi")
            m_value = messageIncoming
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


dexarm1 = Dexarm(port="COM19")
dexarm1.go_home() #Goes to robot home position
dexarm1.sliding_rail_init()
robotConnectedRail = True

initializePressureFlipperArduino()

dexarm1.move_to(316, 54, 40, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
detect() #sets the offset value
#make m_value a string
#parse through m_value and get only the numbers and decimal (maybe use isDigit on each char)
#set offset variable equal to that

dexarm1.move_to(322, 54, dexarm1.get_current_position() - offset, 880, mode ="G0") #move dexarm down to pick up coaster
#adjust the above equation for the picker being lower than the sensor
