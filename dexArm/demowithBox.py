import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import serial

#Add Laser Module:
sys.path.insert(0, 'LaserModule')
import laser_module as l_m

#Add fuzzy feet picker module - to be replaced with a class
from FuzzyFeetPlacementModule import pick_fuzzy_foot, placeFuzzyFeet #module-based implementation

#Add Pressure and Flipper Module:
import pressure_flipper_serial as p_f

#initialize everything
#move rail to right to avoid door opening
#open door
#pick up coaster


stepMovSize = 10
speedRobot = 6000
railStep = 60

dexarm1 = Dexarm(port="COM19")
dexarm2 = Dexarm(port="COM4")
dexarm3 = Dexarm(port="COM6")


l_m.initializeArduino()
dexarm1.go_home() #Goes to robot home position
dexarm2.go_home()
dexarm3.go_home()
dexarm1.sliding_rail_init()
robotConnectedRail = True

#dexarm2.pick_fuzzy_foot()

dexarm3.move_to(-2, 300, 124, mode="G0", feedrate=speedRobot)
dexarm2.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot)
dexarm1.move_to(0, 200, 0, mode="G0", feedrate=speedRobot)

dexarm1.move_to(0, 200, 40, 880, mode="G0", feedrate=speedRobot)
dexarm1.move_to(250, 200, 40, 880, mode="G0", feedrate=speedRobot)
dexarm1.move_to(316, 54, 40, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(322, 54, -8, 880, mode ="G1") #move dexarm down to pick up coaster

l_m.LaserDoorOpen()
l_m.LaserDoorOpen()

dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(316, 54, 40, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(250, 54, 40, 880, mode="G0", feedrate=speedRobot) #move dexarm back
dexarm1.move_to(0, 200, 0, 880, mode="G0", feedrate=speedRobot) #move dexarm to the middle


dexarm1.move_to(0, 200, 0, 350, mode="G0", feedrate=speedRobot) #move dexarm towards laser box
dexarm1.move_to(-395, 60, -35, 300, mode="G0", feedrate=speedRobot) #move dexarm to point towards laser box
dexarm1.move_to(-395, 60, -35, 100, mode="G0", feedrate=speedRobot) #move the dexarm to the laser box
dexarm1.move_to(-385, 50, -35, 40, mode="G0", feedrate=speedRobot) #move the coaster into the laser box
dexarm1.air_picker_stop()
dexarm1.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
dexarm1.move_to(-202, 0, 0, 700, mode="G0") #move dexarm out of laser box
dexarm1.move_to(-201, 0, 0, 700, mode="G1") #move dexarm out of laser box

l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()


#DO LASER ENGRAVING USING DEXARM3
dexarm3.move_to(-2, 300, 123, mode="G1", feedrate=speedRobot)
dexarm3.go_home()
l_m.runLaser(dexarm3)
dexarm3.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot)

l_m.LaserDoorOpen()
l_m.LaserDoorOpen()

dexarm1.move_to(-201, 0, 0, 700, mode="G1", feedrate=speedRobot)
dexarm1.move_to(-201, 0, 0, 600, mode="G0", feedrate=speedRobot)
dexarm1.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm back into the laser box
dexarm1.move_to(-385, 50, -60, 40, mode="G0", feedrate=speedRobot) #pick up the coaster inside the laser box
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm up with the coaster
dexarm1.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
dexarm1.move_to(-202, 0, 0, 300, mode="G0", feedrate=speedRobot) #move dexarm out of laser box



dexarm1.move_to(0, 200, 0, 300, mode="G0", feedrate=speedRobot) #move coaster to flipper station
dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #move coaster to flipper station
dexarm1.move_to(-61, 342, -65, 0, mode="G0", feedrate=speedRobot)
dexarm1.air_picker_stop()
dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #retract arm
#FLIP THE COASTER USING ARDUINO
p_f.initializePressureFlipperArduino()
p_f.FlipperStationGo()
dexarm1.move_to(57, 344, -93, 0, mode="G0", feedrate=speedRobot) #pick up the coaster from the flipped table
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(57, 344, -80, 0, mode="G0", feedrate=speedRobot) #move up the coaster from the flipped table
dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #retract arm



dexarm1.move_to(0, 200, 0, 880, mode="G0", feedrate=speedRobot) #move arm to fuzzy feet putter area
dexarm1.move_to(15, 256, -85, 880, mode="G0", feedrate=speedRobot) #move the coaster to the fuzzy feet putter area
dexarm1.move_to(15, 303, -85, 880, mode="G0", feedrate=speedRobot)
dexarm1.air_picker_stop()
dexarm1.move_to(0, 200, 0, 200, mode="G0", feedrate=speedRobot) #retract arm
dexarm1.move_to(0, 200, 0, 200) #for waiting


'''
#PICK UP FUZZY FEET FROM THE PAPER USING DEXARM2
dexarm2.move_to(0, 247, 0, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(0, 247, -97, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(0, 247, 0, mode="G0", feedrate=speedRobot) #lift up fuzzy feet

dexarm2.move_to(-191, 204, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-191, 204, -89, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-191, 204, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet



dexarm2.move_to(-1, 319, 0, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-1, 319, -97, mode="G0", feedrate=speedRobot) #pick fuzzy feet
dexarm2.move_to(-1, 319, 0, mode="G0", feedrate=speedRobot) #lift up fuzzy feet

dexarm2.move_to(-222, 148, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-222, 148, -89, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-222, 148, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet



dexarm2.move_to(-27, 295, 0, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-27, 295, -97, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-27, 295, 0, mode="G0", feedrate=speedRobot) #lift up fuzzy feet

dexarm2.move_to(-248, 199, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-248, 199, -89, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-248, 199, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

dexarm2.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot)
'''

#Use module implementation
pick_indices = [(1, 1), (2, 1), (3, 1)]

#the actual function call 
placeFuzzyFeet(dexarm2, pick_indices, 3) #Call dexarm module 

dexarm2.move_to(-200, 30, 0) #for waiting



dexarm1.move_to(10, 303, 0, 880, mode="G1", feedrate=speedRobot) #pick up coaster from fuzzy feet area
dexarm1.move_to(10, 303, -88, 880, mode="G0", feedrate=speedRobot) #pick up coaster from fuzzy feet area
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(10, 250, -88, 880, mode="G0", feedrate=speedRobot) #move coaster out
dexarm1.move_to(10, 250, 0, 880, mode="G0", feedrate=speedRobot) #move coaster out



dexarm1.move_to(13, 223, -9, 360, mode="G0", feedrate=speedRobot) #move to presser station
dexarm1.move_to(13, 244, -83, 360, mode="G0", feedrate=speedRobot) #lower to presser station
dexarm1.move_to(13, 294, -83, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarm1.move_to(13, 294, -75, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarm1.air_picker_stop()
dexarm1.move_to(13, 238, -75, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarm1.move_to(13, 238, -85, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarm1.move_to(13, 300, -85, 360, mode="G0", feedrate=speedRobot) #push coaster into presser station
dexarm1.move_to(13, 238, -85, 360, mode="G0", feedrate=speedRobot) #move arm back
dexarm1.move_to(13, 223, -9, 360, mode="G1", feedrate=speedRobot) #move arm up
dexarm1.move_to(13, 222, -9, 360, wait = True) #move arm up
dexarm1.move_to(13, 220, -9, 360, wait = True) #move arm up
p_f.PressureStationGo()

dexarm1.move_to(-1, 283, -70, 360, mode="G0", feedrate=speedRobot) #move arm above pick up area
dexarm1.move_to(-1, 283, -90, 360, mode="G0", feedrate=speedRobot) #move arm down to pick up coaster
dexarm1.air_picker_pick() #pick up coaster
dexarm1.move_to(-1, 260, -90, 360, mode="G0", feedrate=speedRobot) #move arm out with coaster 
dexarm1.move_to(-4, 228, -30, 360, mode="G0", feedrate=speedRobot) #move arm up

dexarm1.move_to(295, 234, 46, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(295, 234, 46, 881, wait = True) #move dexarm to the right above coasters
dexarm1.air_picker_stop()

l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
l_m.LaserDoorClose()