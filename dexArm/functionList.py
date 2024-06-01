import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import serial

stepMovSize = 10
speedRobot = 6000
railStep = 60

def initializePressureFlipperArduino(wait=True):
    global pressure_flipperArduinoSerial
    port = "COM25"
    baud = 115200
    pressure_flipperArduinoSerial = serial.Serial(port, baud, timeout = 0.1)
    global serial_line 
    serial_line = pressure_flipperArduinoSerial.readline()
    if wait == True:
        time.sleep(3)

def pickCoaster(): #makes the picker dexarm pick up a coaster


def moveTo(self): #moves picker dexarm to the specified station
    


def flipperOperate():
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


def presserOperate():
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


def laserCutOperate(self):
    self.go_home()
    l_m.runLaser(self)
    self.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot)

def fuzzyOperate():
    self.move_to(10, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(10, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(10, 296, -86) #pick up fuzzy feet
    self.move_to(-191, 204, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-191, 204, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-191, 204, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

    self.move_to(-17, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(-17, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(-17, 296, -86) #pick up fuzzy feet
    self.move_to(-222, 148, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-222, 148, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-222, 148, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

    self.move_to(-43, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(-43, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
    self.move_to(-43, 296, -86) #pick up fuzzy feet
    self.move_to(-248, 199, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-248, 199, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
    self.move_to(-248, 199, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

    self.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot)
    self.move_to(-200, 30, 0) #for waiting