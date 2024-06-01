import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys

#Open communication with dexarm
#Windows: 
dexarm2 = Dexarm(port="COM6")
dexarm2.go_home()

dexarm2.move_to(42,213,-8,feedrate=1000,wait=True)
dexarm2.air_picker_pick()


dexarm2.move_to(-86,356,-33,feedrate=1000,wait=True)
dexarm2.air_picker_stop()

dexarm2.move_to(42,213,-8,feedrate=1000,wait=True)

dexarm2.move_to(44,210,-40,feedrate=1000,wait=True)
dexarm2.air_picker_pick()
dexarm2.move_to(44,210,0,feedrate=1000,wait=True)

dexarm2.move_to(-86,356,-33,feedrate=1000,wait=True)
dexarm2.air_picker_stop()

dexarm2.move_to(42,213,-8,feedrate=1000,wait=True)