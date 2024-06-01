import sys
# Add Movement module
sys.path.insert(0, "MovementModule")
from pydexarm import Dexarm
import time
import keyboard
import sys
import serial
import laser_module as l_m

#Add Laser Module:
sys.path.insert(0, 'LaserModule')

#Alex's Modules
from PickerLoadingModule import grabCoaster #Function for grabbing coaster from loading area using sensor. 
from PickerUnloadingModule import deposit_coaster #Function for going to the correct spot, then dropping a coaster. 
from FuzzyFeetPlacementModule import pick_fuzzy_foot, placeFuzzyFeet #module-based implementation
from FlipperStationModule import flipCoaster #new function to flip coaster, then grab it again
from PressureStationModule import pressCoaster #Pressure station module. 
from AddFuzzyFeetModule import placeFuzzyFeet #Fuzzy feet placement module
from InitializationModule import initializeWorkcell, goHomes
from laserModule import laserDropOff, laserPickUp


#Define Dexarm objects
dexarmPicker = Dexarm(port="COM19") #COM port for Picker ARM
dexarmAdhesive = Dexarm(port="COM4") #COM port for Adhesive ARM 
dexarmLaser = Dexarm(port="COM6") #COM port for laser ARM

fileName = ""
n = 1 #laser counter
l = 1 #loops wanted

initializeWorkcell(dexarmPicker,dexarmAdhesive,dexarmLaser) #Ensure all three arms are properly initialized. 

while l <=4:
    # MAIN BODY
    goHomes(dexarmPicker,dexarmAdhesive,dexarmLaser)
    #DONE: Add abstracted fuzzy feet placement. 
    grabCoaster(dexarmPicker) #Load a coaster. This uses the sensor and checks for success automatically. 

    #TODO: Add module for laser here. 
    l_m.LaserDoorOpen()
    l_m.LaserDoorOpen()

    laserDropOff(dexarmPicker, dexarmLaser)

    l_m.LaserDoorClose()
    l_m.LaserDoorClose()

    if n == 1: 
        fileName = "outputGcode1.txt"
        n += 1
    if n == 2: #everything past 1 needs to be created still
        fileName = "outputGcode2.txt"
        n += 1
    if n == 3:
        fileName = "outputGcode3.txt"
        n += 1
    if n == 4:
        fileName = "outputGcode4.txt"
        n += 1

    time.sleep(5)
    l_m.runLaser(dexarmLaser, fileName)

    l_m.LaserDoorOpen()
    l_m.LaserDoorOpen()

    laserPickUp(dexarmPicker, dexarmLaser)

    #DONE: Added in abstracted module for flipping. 
    flipCoaster(dexarmPicker) #Call the module that flips the coaster. 

    #DONE: Added in abstracted module for placing fuzzy feet.
    pick_indices = [(1, 1), (2, 1), (3, 1)] #Manually defined for now. 

    #placeFuzzyFeet(dexarmPicker,dexarmAdhesive, pick_indices)
    placeFuzzyFeet(dexarmPicker, pick_indices, 3)
    #DONE: Added abstracted module for pressing coasters. 
    pressCoaster(dexarmPicker)

    #DONE: Added abstracted module for unloading coasters. 
    deposit_coaster(dexarmPicker)

    #NOTE: Laser door doesn't close at the end of its sequence in current iteration? Let's fix that. 
    l_m.LaserDoorClose()
    l_m.LaserDoorClose()
    l += 1 #update counter