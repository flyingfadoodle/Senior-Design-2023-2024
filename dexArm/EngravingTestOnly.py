from pydexarm import Dexarm
import pydexarmCustom
import laser_module as l_m
import sys
sys.path.insert(0, 'LaserModule')
sys.path.insert(0, "MovementModule")

#Define Dexarm objects
dexarmPicker = Dexarm(port="COM19") #COM port for Picker ARM
dexarmAdhesive = Dexarm(port="COM4") #COM port for Adhesive ARM 
dexarmLaser = Dexarm(port="COM6") #COM port for laser ARM

#Variables related to laser
coasterDesign = 4 #Which coaster variant are we doing
loops = 1 #loops wanted

#MAIN BODY OF CODE

pydexarmCustom.initializeWorkcell(dexarmPicker,dexarmAdhesive,dexarmLaser) #Ensure all three arms are properly initialized. 

while loops <=12:
    #loops += 1 #Increase the loop counter. We can change this at the start since it's only used to know when t stop. coasterDesign actually controls which design variant we're using

    # MAIN BODY

    #goHomes(dexarmPicker,dexarmAdhesive,dexarmLaser) This will cause problems when looping. We'll need a function which re-sets the arms to their idle positions. 
    #Also, most modules home somewhere in their sequences. Let

    #DONE: Add abstracted fuzzy feet placement. 
    pydexarmCustom.grabCoaster(dexarmPicker) #Load a coaster. This uses the sensor and checks for success automatically. 

    #TODO: Check to make sure the new module, EngraveCoasterModule, actually works. 

    #NOTE: The laser engraver currently doesn't run within EngraveCoaster. It is commented out while we get the door working. 
    pydexarmCustom.EngraveCoaster(dexarmPicker,dexarmLaser,coasterDesign) #dexarm, dexarm, desired Coaster index. 

    coasterDesign += 1 #Increment desired design by one 

    coasterDesign = 1 if coasterDesign > 4 else coasterDesign #Loop back around to the fourth coaster design if we've gone too far. 

    pydexarmCustom.deposit_coaster(dexarmPicker)

    loops += 1 #update counter