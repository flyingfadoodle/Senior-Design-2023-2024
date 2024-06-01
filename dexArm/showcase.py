import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys

#steps
# 1. pick up item from starting area
# 2. move item to first station
# 3. item is operated on
# 4. move item to second station
# 5. item is operated on
# 6. move item to deposit area

stepMovSize = 10
speedRobot = 6000
railStep = 60

def delay():
    print(stepMovSize)

dexarm1 = Dexarm(port="COM19")
dexarm2 = Dexarm(port="COM4")
#dexarm3 = Dexarm(port="COM6")
dexarm1.sliding_rail_init()
robotConnectedRail = True

dexarm1.go_home()#Goes to robot home position
dexarm2.go_home()
#dexarm3.go_home()


#WHENVER THE PICKER ARM MOVES HAVE THAT BE A NEW FUNCTION BECAUSE THAT MAKES EVERYTHING ELSE WAIT
#or just call an empty function and artifically stall
#bc in frameDemo code the rest of the code waits until the moving rail function call is completed before going

while True:
     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot) #pick up item from starting area
     dexarm1.move_to(-218, 306, -77, 0, mode="G0", feedrate=speedRobot) #pick up item from starting area
     dexarm1.air_picker_pick()

     dexarm2.move_to(-175, 61, -35, mode="G0", feedrate=speedRobot) #station 1 arm moves aside
#dexarm3.move_to(-218.45, 95.23, -39.1, mode="G0", feedrate=speedRobot) #station 2 arm moves aside

     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot) #moves item up to avoid collisions
     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #move item to first station
     dexarm1.move_to(5, 235, -98, 120, mode="G0", feedrate=speedRobot) #lowers item on first station
     dexarm1.air_picker_stop()

     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #moves picker arm up to avoid collisions
     dexarm1.move_to(-227, 65, 0, 120, mode="G0", feedrate=speedRobot) #picker arm moves aside
#function call to delay

# dexarm2.move_to(-32, 211, -68, mode="G0", feedrate=speedRobot) #station 1 arm operates
# dexarm2.move_to(-175, 61, -35, mode="G0", feedrate=speedRobot) #station 1 arm moves aside
     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #moves picker arm up to avoid collisions
     dexarm1.move_to(5, 235, -98, 120, mode="G0", feedrate=speedRobot) #picker arm picks up item from station 1
     dexarm1.air_picker_pick()
     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #moves item up to avoid collisions

     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #move item to second station
     dexarm1.move_to(5, 235, -98, 720, mode="G0", feedrate=speedRobot) #lowers item on second station
     dexarm1.air_picker_stop()
     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot) #picker arm moves back to start
     dexarm1.move_to(-218, 306, -77, 0, mode="G0", feedrate=speedRobot) #picker arm lowers at start
     dexarm1.air_picker_pick()
     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot) #picker arm moves up to avoid collisions
# dexarm3.move_to(-2.78, 226.59, -73.06, mode="G0", feedrate=speedRobot) #station 2 arm operates

     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #move item to first station
     dexarm1.move_to(5, 235, -98, 120, mode="G0", feedrate=speedRobot) #move new item to first station
     dexarm1.air_picker_stop()
     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

# dexarm3.move_to(-218.45, 95.23, -39.1, mode="G0", feedrate=speedRobot) #station 2 arm moves aside

     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #move picker arm to second station
     dexarm1.move_to(5, 235, -98, 720, mode="G0", feedrate=speedRobot) #lowers picker arm on second station

# dexarm2.move_to(-32, 211, -68, mode="G0", feedrate=speedRobot) #station 1 arm operates
     dexarm1.air_picker_pick()
     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

     dexarm1.move_to(294, 235, -20, 840, mode="G0", feedrate=speedRobot) #picker arm moves item to end
     dexarm1.move_to(294, 235, -98, 840, mode="G0", feedrate=speedRobot) #picker arm lowers at the end
     dexarm1.air_picker_stop()
# dexarm2.move_to(-175, 61, -35, mode="G0", feedrate=speedRobot) #station 1 arm moves aside
     dexarm1.move_to(294, 235, -20, 840, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #picker arm picks up item at station 1
     dexarm1.move_to(5, 235, -98, 120, mode="G0", feedrate=speedRobot) #picker arm lowers on station 1
     dexarm1.air_picker_pick()
     dexarm1.move_to(5, 235, -20, 120, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm moves new item to second station
     dexarm1.move_to(5, 235, -98, 720, mode="G0", feedrate=speedRobot) #picker arm lowers on second station
     dexarm1.air_picker_stop()
     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm moves new item to second station
     dexarm1.move_to(-227, 65, 0, 720, mode="G0", feedrate=speedRobot) #picker arm moves aside

# dexarm3.move_to(-2.78, 226.59, -73.06, mode="G0", feedrate=speedRobot) #station 2 arm operates
# dexarm3.move_to(-218.45, 95.23, -39.1, mode="G0", feedrate=speedRobot) #station arm 2 moves aside
     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm moves to second station
     dexarm1.move_to(5, 235, -98, 720, mode="G0", feedrate=speedRobot) #picker arm lowers on second station
     dexarm1.air_picker_pick()
     dexarm1.move_to(5, 235, -20, 720, mode="G0", feedrate=speedRobot) #picker arm lifts up to avoid collisions

     dexarm1.move_to(294, 235, -20, 840, mode="G0", feedrate=speedRobot) #picker arm moves item to end -88 adjusted for the second picker
     dexarm1.move_to(294, 235, -88, 840, mode="G0", feedrate=speedRobot) #picker arm moves item to end -88 adjusted for the second picker
     dexarm1.air_picker_stop()


#put back
     dexarm1.move_to(294, 235, -20, 840, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 235, -88, 840, mode="G0", feedrate=speedRobot)
     dexarm1.air_picker_pick()
     dexarm1.move_to(294, 190, -20, 840, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 190, -20, 100, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(-218, 306, -77, 0, mode="G0", feedrate=speedRobot) 
     dexarm1.air_picker_stop()
     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 190, -20, 100, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 235, -20, 840, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 235, -98, 840, mode="G0", feedrate=speedRobot)
     dexarm1.air_picker_pick()
     dexarm1.move_to(294, 190, -20, 840, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(294, 190, -20, 100, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(-218, 306, -20, 0, mode="G0", feedrate=speedRobot)
     dexarm1.move_to(-218, 306, -77, 0, mode="G0", feedrate=speedRobot) 
     dexarm1.air_picker_stop()