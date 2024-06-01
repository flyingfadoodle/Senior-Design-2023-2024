import pydexarmCustom
from pydexarm import Dexarm
import pressure_flipper_serial as p_f
import time

dexarmPicker = Dexarm(port="COM19") #COM port for Picker ARM
dexarmAdhesive = Dexarm(port="COM4") #COM port for Adhesive ARM 
#dexarmLaser = Dexarm(port="COM6") #COM port for laser ARM

#pydexarmCustom.initializeWorkcell(dexarmPicker,dexarmAdhesive,dexarmLaser)

#p_f.initializePressureFlipperArduino()

#pydexarmCustom.grabCoaster(dexarmPicker)

#pydexarmCustom.pressCoaster(dexarmPicker)

#pydexarmCustom.deposit_coaster(dexarmPicker)
dexarmAdhesive.go_home()
dexarmAdhesive.move_to(-200, 30, 0, mode="G0", feedrate=6000) #Move adhesive arm out of the way. 

time.sleep(5) #Give the picker a chance to get out of the way. 

dexarmPicker.go_home() #Goes to robot home position
   
   #Initialize the sliding rail. This way, we can make sure the door is closed prior to starting anything. 
dexarmPicker.sliding_rail_init() #skipped rail init for time reasons 

#Finish init 


loops = 1

while loops <=4: 

   # pick_indices = pydexarmCustom.assign_pick_indices(loops) #This will break once loops exceeds 4. This is bad, but also intentional. 
    pick_indices = [(1, 1), (2, 1), (3, 1)] #Manually defined for now. 


    pydexarmCustom.grabCoaster(dexarmPicker)

    pydexarmCustom.applyFuzzyFeet(dexarmPicker,dexarmAdhesive,pick_indices)

    pydexarmCustom.deposit_coaster(dexarmPicker)

    loops += 1



#pydexarmCustom.pick_fuzzy_foot(dexarmAdhesive,3,2) #NOTE: pick_fuzzy_foot has an arbitrary Z-offset atm for testing reasons. 

#pydexarmCustom.applyFuzzyFeet(dexarmPicker,dexarmAdhesive,pick_indices)