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
dexarm2 = Dexarm(port="COM6")
dexarm1.go_home()
dexarm2.go_home()

def robotDown(stepIncrement, feedrate):
    dexarm1._send_cmd("G92 X0 Y0 Z0\r"); #Zeros position
    dexarm1.move_to(z=-stepIncrement,feedrate=feedrate)
    dexarm1._send_cmd("G92.1\r");#Resets to home

robotDown(60,8000)

dexarm2.move_to(42,213,-8,feedrate=1000,wait=False)
dexarm2.air_picker_pick()

dexarm1.move_to(115,300,-127,feedrate = 1000, wait = False)

dexarm2.move_to(-86,356,-33,feedrate=1000,wait=False)
dexarm2.air_picker_stop()

dexarm1.move_to(-172,300,-127, feedrate=1000, wait=False)

dexarm2.move_to(42,213,-8,feedrate=1000,wait=False)

dexarm1.move_to(115,300,-127,feedrate = 2000, wait = False)

dexarm2.move_to(44,210,-40,feedrate=1000,wait=False)
dexarm2.air_picker_pick()
dexarm2.move_to(44,210,0,feedrate=1000,wait=False)

dexarm2.move_to(-86,356,-33,feedrate=1000,wait=False)
dexarm2.air_picker_stop()

dexarm1.move_to(-172,300,-127, feedrate=1000, wait=False)

dexarm2.move_to(42,213,-8,feedrate=1000,wait=False)