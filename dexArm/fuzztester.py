import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys

stepMovSize = 10
speedRobot = 2000 #origionall 6000
#speedPick = 200 #lower speed for fine motions
railStep = 60
dexarm2 = Dexarm(port="COM4")

dexarm2.go_home()

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
dexarm2.move_to(-200, 30, 0) #for waiting