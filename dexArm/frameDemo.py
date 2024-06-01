import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys


#Open communication with dexarm
#Windows: 
dexarm1 = Dexarm(port="COM19")
dexarm2 = Dexarm(port="COM4")

#Initialize components
dexarm1.sliding_rail_init()
stepMovSize = 10
speedRobot = 6000
railStep = 20

#function to move the sliding rail num amount of times
def moveRailForward(num):
    for x in range(0,num):
        #dexarm1._send_cmd("G92 X0 Y0 Z0\r"); #Zeros position
        _,_,_,eRail,_,_,_ =dexarm1.get_current_position()
        print(eRail)
        dexarm1.move_to(e=railStep+eRail,feedrate=speedRobot) #currently only dexarm 1 is on a rail

def moveRailBack(num):
    for x in range(0,num):
        #dexarm1._send_cmd("G92 X0 Y0 Z0\r"); #Zeros position
        _,_,_,eRail,_,_,_ =dexarm1.get_current_position()
        print(eRail)
        dexarm1.move_to(e=-railStep+eRail,feedrate=speedRobot) #currently only dexarm 1 is on a rail

dexarm1.go_home()
dexarm2.go_home()


dexarm1.move_to(-300, 181, -105, mode="G0", feedrate=speedRobot) #Pick up item from starting area
dexarm1.air_picker_pick() #activate picker
dexarm1.move_to(0, 231, -12, mode="G0", feedrate=speedRobot) #adjust arm back to center
dexarm2.move_to(-168, 81, 0) #Move aside so arms don't collide

moveRailForward(24) #Move to first station

dexarm1.move_to(0, 273, -108, mode="G0", feedrate=speedRobot) #move arm in position to drop item
dexarm1.air_picker_stop() #drop item

dexarm1.move_to(-165, 179, 22, mode="G0", feedrate=speedRobot) #move arm aside so other arm can do work

dexarm2.move_to(250, 200, -93, mode="G0", feedrate=speedRobot) #arm 2 does work
dexarm2.move_to(-212, 131, 0, mode="G0", feedrate=speedRobot) #adjust arm back to center

dexarm1.move_to(0, 273, -108, mode="G0", feedrate=speedRobot) #move arm back to pick up item
dexarm1.air_picker_pick()
dexarm1.move_to(0, 231, -12, mode="G0", feedrate=speedRobot) #adjust arm back to center

moveRailBack(24) #move back to starting area

dexarm1.move_to(-300, 181, -105, mode="G0", feedrate=speedRobot) #move arm to drop off item
dexarm1.air_picker_stop() #drop item
dexarm1.move_to(0, 231, -12, mode="G0", feedrate=speedRobot) #adjust arm back to center

#dexarm1.move_to(0, 413, 0, mode="G0", feedrate=speedRobot) #Adjust to center of wingspan to place item
#dexarm1.move_to(0, 238, 0, mode="G0", feedrate=speedRobot) #Bring back arm so it can move past first station

#moveRail(15) #Move to second station

