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
coasterDesign = 1 #Which coaster variant are we doing
loops = 1 #loops wanted

#MAIN BODY OF CODE


pydexarmCustom.initializeWorkcell(dexarmPicker,dexarmAdhesive,dexarmLaser) #Ensure all three arms are properly initialized. 

while loops <=4:
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

    """
    Key for coaster indices
    1 = we
    2 = haven't
    3 = defined
    4 = these
    5 = yet
    """

    #DONE: Added in abstracted module for flipping. 
    pydexarmCustom.flipCoaster(dexarmPicker) #Call the module that flips the coaster. 

    #DONE: Added in abstracted module for placing fuzzy feet.

    #TODO: Add something to cylce through pick indices, given a single starting index. 

    
    pick_indices = [(1, 1), (2, 1), (3, 1)] #Manually defined for now. 

    #placeFuzzyFeet(dexarmPicker,dexarmAdhesive, pick_indices)
    pydexarmCustom.applyFuzzyFeet(dexarmPicker, dexarmAdhesive, pick_indices)

    #DONE: Added abstracted module for pressing coasters. 
    pydexarmCustom.pressCoaster(dexarmPicker)

    #DONE: Added abstracted module for unloading coasters. 
    pydexarmCustom.deposit_coaster(dexarmPicker)

    #dexarmPicker.move_to(320, 57, 120, 20, mode="G0", feedrate=6000)
    #pydexarmCustom.goHomes(dexarmPicker, dexarmAdhesive, dexarmLaser)
    #pydexarmCustom.initialize_picker_arm(dexarmPicker)
    loops += 1 #update counter