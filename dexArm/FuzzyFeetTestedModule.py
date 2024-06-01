from FuzzyFeetPlacementModule import pick_fuzzy_foot, placeFuzzyFeet #module-based implementation

import sys #copy pasted, ignore the inefficiency
import time
import math
from pydexarm import Dexarm
#from pydexarm import ExtendedDexarm #not going to be using class extensions 

dexarm = Dexarm(port="COM4")
dexarm.go_home()
pick_indices = [(2, 1), (4, 1), (3, 1)]

#the actual function call 
placeFuzzyFeet(dexarm, pick_indices, 3) #okay, so calling the module works, but trying to use the added functions to the dexArm class does not. Weird. 

#dexarm.pick_fuzzy_foot(1,1) #currently causes the arm to hang, requiring a restart
#dexarm.placeFuzzyFeet(pick_indices,3) #also causes the arm to hang, requiring a restart