import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys

#Add Laser Module:
sys.path.insert(0, 'LaserModule')
import laser_module as l_m
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

l_m.initializeArduino()
p_f.initializePressureFlipperArduino()
dexarm1.go_home() #Goes to robot home position
dexarm2.go_home()
dexarm1.sliding_rail_init()
robotConnectedRail = True

dexarm2.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot)
dexarm1.move_to(0, 200, 0, mode="G0", feedrate=speedRobot)
dexarm1.move_to(0, 200, 0, 880, mode="G0", feedrate=speedRobot)
print("hello")
dexarm1.move_to(250, 200, 0, 880, mode="G0", feedrate=speedRobot)
print("hello2")
dexarm1.move_to(250, 57, 0, 880, mode="G0", feedrate=speedRobot) #HAVE TO DO THIS STUFF IN STEPS FOR SOME REASON WHEN CHANGING DIRECTIONS BY A LOT 
dexarm1.move_to(316, 54, 10, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(316, 54, -9, 880) #move dexarm down to pick up coaster

l_m.LaserDoorOpen()
l_m.LaserDoorOpen()

dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(316, 54, 10, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(250, 54, 10, 880, mode="G0", feedrate=speedRobot) #move dexarm back
dexarm1.move_to(0, 200, 0, 880, mode="G0", feedrate=speedRobot) #move dexarm to the middle
dexarm1.move_to(0, 200, 0, 350, mode="G0", feedrate=speedRobot) #move dexarm towards laser box
dexarm1.move_to(-395, 60, -35, 300, mode="G0", feedrate=speedRobot) #move dexarm to point towards laser box
dexarm1.move_to(-395, 60, -35, 100, mode="G0", feedrate=speedRobot) #move the dexarm to the laser box
dexarm1.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the coaster into the laser box
dexarm1.air_picker_stop()
dexarm1.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
dexarm1.move_to(-202, 0, 0, 300, mode="G0", feedrate=speedRobot) #move dexarm out of laser box

#DO LASER ENGRAVING USING DEXARM3

dexarm1.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm back into the laser box
dexarm1.move_to(-385, 50, -60, 40, mode="G0", feedrate=speedRobot) #pick up the coaster inside the laser box
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm up with the coaster
dexarm1.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
dexarm1.move_to(-202, 0, 0, 300, mode="G0", feedrate=speedRobot) #move dexarm out of laser box



dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #move coaster to flipper station
dexarm1.move_to(-125, 345, -70, 0, mode="G0", feedrate=speedRobot) #move coaster to flipper station
dexarm1.air_picker_stop()
dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #retract arm
time.sleep(3)
p_f.FlipperStationGo() #FLIP THE COASTER USING ARDUINO
dexarm1.move_to(0, 345, -81, 0, mode="G0", feedrate=speedRobot) #pick up the coaster from the flipped table
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(0, 200, 0, 0, mode="G0", feedrate=speedRobot) #retract arm



dexarm1.move_to(0, 200, 0, 880, mode="G0", feedrate=speedRobot) #move arm to fuzzy feet putter area
dexarm1.move_to(10, 256, -85, 880, mode="G0", feedrate=speedRobot) #move the coaster to the fuzzy feet putter area
dexarm1.move_to(10, 303, -85, 880, mode="G0", feedrate=speedRobot)
dexarm1.air_picker_stop()
dexarm1.move_to(0, 200, 0, 200, mode="G0", feedrate=speedRobot) #retract arm
dexarm1.move_to(0, 200, 0, 200) #for waiting



#PICK UP FUZZY FEET FROM THE PAPER USING DEXARM2
dexarm2.move_to(10, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(10, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(10, 296, -86) #pick up fuzzy feet
dexarm2.move_to(-191, 204, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-191, 204, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-191, 204, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

dexarm2.move_to(-17, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-17, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-17, 296, -86) #pick up fuzzy feet
dexarm2.move_to(-222, 148, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-222, 148, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-222, 148, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

dexarm2.move_to(-43, 296, -86, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-43, 296, -107, mode="G0", feedrate=speedRobot) #pick up fuzzy feet
dexarm2.move_to(-43, 296, -86) #pick up fuzzy feet
dexarm2.move_to(-248, 199, -80, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-248, 199, -96, mode="G0", feedrate=speedRobot) #place fuzzy feet
dexarm2.move_to(-248, 199, -70, mode="G0", feedrate=speedRobot) #place fuzzy feet

dexarm2.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot)
dexarm2.move_to(-200, 30, 0) #for waiting



dexarm1.move_to(10, 303, -88, 880, mode="G0", feedrate=speedRobot) #pick up coaster from fuzzy feet area
dexarm1.air_picker_pick() #pick up the coaster
dexarm1.move_to(10, 250, -88, 880, mode="G0", feedrate=speedRobot) #move coaster out
dexarm1.move_to(10, 250, 0, 880, mode="G0", feedrate=speedRobot) #move coaster out



dexarm1.move_to(7, 223, -9, 360, mode="G0", feedrate=speedRobot) #move to presser station
dexarm1.move_to(7, 244, -83, 360, mode="G0", feedrate=speedRobot) #lower to presser station
dexarm1.move_to(7, 294, -83, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarm1.move_to(7, 294, -75, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarm1.air_picker_stop()
dexarm1.move_to(7, 238, -75, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarm1.move_to(7, 238, -85, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarm1.move_to(7, 300, -85, 360, mode="G0", feedrate=speedRobot) #push coaster into presser station
time.sleep(5)
p_f.PressureStationGo() #press and push coaster back out using arduino




dexarm1.move_to(316, 54, 10, 880, mode="G0", feedrate=speedRobot) #move dexarm to the right above coasters
dexarm1.move_to(316, 54, 10, 881, wait = True) #move dexarm to the right above coasters
dexarm1.air_picker_stop()
l_m.LaserDoorClose()
l_m.LaserDoorClose()
