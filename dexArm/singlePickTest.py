import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import time #for waits


speedRobot = 4000 #origionall 6000
speed2Robot = 100 #lower speed for fine motions
dexarm2 = Dexarm(port="COM4")

dexarm2.go_home()

pickX = -51;
pickY = 220.5; 
pickZ = -96; 
offset = 5; #offset when hovering
offset2 = 1; #offset when sliding forwards when picking

dexarm2.move_to(pickX, pickY, 0, mode="G1", feedrate=speedRobot) #hover above fuzzy feet
dexarm2.move_to(pickX, pickY, pickZ+offset, mode="G1", feedrate=speedRobot) #hover above fuzzy feet
dexarm2.move_to(pickX, pickY, pickZ, mode="G1", feedrate=speed2Robot) #pick fuzzy feet
#time.sleep(0.5) #Hold for half a second prior to sliding forwards
dexarm2.move_to(pickX, pickY+offset2, pickZ, mode="G1", feedrate=speed2Robot) #attempt to slide fowards 0.5mm 
dexarm2.move_to(pickX, pickY+offset2, pickZ+offset, mode="G1", feedrate=speed2Robot) #lift part-way up, slowly 
dexarm2.move_to(pickX, pickY+offset2, 0, mode="G1", feedrate=speedRobot) #lift fuzzy feet up remainer of height