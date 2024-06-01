import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import serial

#Open communication with dexarm
#Windows: 
#dexarm1 = Dexarm(port="COM6")
dexarm1 = Dexarm(port="COM4")
#dexarm1 = Dexarm(port="COM19")

def robotPrintLocation():
    dexarm1._send_cmd("G92.1\r");#Resets
    x,y,z,e,_,_,_ =dexarm1.get_current_position()
    print(x,y,z,e, "mm")


#First Initialize Dexarm:p
#Factory Settings: Home -> (0,300,0)
dexarm1.go_home()#Goes to robot home position


robotPrintLocation() #Where are we? 

dexarm1.move_to(100, 247, 0, mode="G0", feedrate=2000) #Go somewhere

robotPrintLocation() #Check where we are 

dexarm1.go_home()#Try to go home again

robotPrintLocation() #Where are we now? 