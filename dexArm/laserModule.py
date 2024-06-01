from TOFSensorModule import get_sensor_height, close_sensor
from PickVerificationModule import pickStatus #For fault detection. 
from ErrorHandlingModule import stopWorkcell

speedRobot = 6000


def laserDropOff(dexarmPicker, dexarmLaser):
    dexarmLaser.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot) #move laser dexarm up
    dexarmPicker.move_to(0, 200, 0, 350, mode="G0", feedrate=speedRobot) #move dexarmPicker towards laser box
    dexarmPicker.move_to(-395, 60, -35, 300, mode="G0", feedrate=speedRobot) #move dexarmPicker to point towards laser box
    dexarmPicker.move_to(-395, 60, -35, 100, mode="G0", feedrate=speedRobot) #move the dexarmPicker to the laser box
    dexarmPicker.move_to(-385, 50, -35, 40, mode="G0", feedrate=speedRobot) #move the coaster into the laser box
    dexarmPicker.air_picker_stop()
    dexarmPicker.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarmPicker back to move out of laser box
    dexarmPicker.move_to(-202, 0, 0, 700, mode="G0") #move dexarmPicker out of laser box
    dexarmPicker.move_to(-201, 0, 0, 700, mode="G1") #move dexarm out of laser box

def laserPickUp(dexarmPicker, dexarmLaser):
    dexarmLaser.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot) #move laser dexarm up
    dexarmPicker.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm back into the laser box
    dexarmPicker.move_to(-385, 50, -60, 40, mode="G0", feedrate=speedRobot) #pick up the coaster inside the laser box
    dexarmPicker.air_picker_pick() #pick up the coaster
    dexarmPicker.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm up with the coaster
    dexarmPicker.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
    dexarmPicker.move_to(-202, 0, 0, 300, mode="G0", feedrate=speedRobot) #move dexarm out of laser box