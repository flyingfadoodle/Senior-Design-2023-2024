#A simple test code for figure out what the heck a set of code is doing

from PickerLoadingModule import grabCoaster, initialize_picker_arm
from PickerUnloadingModule import deposit_coaster
from FlipperStationModule import flipCoaster #new function to flip coaster, then grab it again
from FuzzyFeetPlacementModule import pick_fuzzy_foot, placeFuzzyFeet #module-based implementation
from PressureStationModule import pressCoaster
from AddFuzzyFeetModule import applyFuzzyFeet
from InitializationModule import initializeWorkcell

from pydexarm import Dexarm
import time


import pressure_flipper_serial as p_f #Needed due to the lack of an existing initialization function


dexarmPicker = Dexarm(port='COM19')

dexarmAdhesive = Dexarm(port="COM4") #Declare the fuzzy feet picker, and have it do its thing. 

speedRobot = 6000; #this is here so other codes copy-pasted here actually work

# Body 
#initialize_picker_arm(dexarmPicker) #Optionally, initialize

 
#Make sure that pressure-flipped is initialized 
#p_f.initializePressureFlipperArduino()

grabCoaster(dexarmPicker) #Grab a coaster... then do stuff with it

pick_indices = [(1, 1), (2, 1), (3, 1)] #Manually defined for now. 

applyFuzzyFeet(dexarmPicker,dexarmAdhesive, pick_indices)

#pressCoaster(dexarmPicker) #Attempt to press coaster with module. 

deposit_coaster(dexarmPicker)

dexarmPicker.air_picker_stop() #Shush. If we do succeed, make less noise. 

'''
#The code straight from the pressure station. 
dexarmPicker.move_to(13, 223, -9, 360, mode="G0", feedrate=speedRobot) #move to presser station
dexarmPicker.move_to(13, 244, -83, 360, mode="G0", feedrate=speedRobot) #lower to presser station
dexarmPicker.move_to(13, 294, -83, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarmPicker.move_to(13, 294, -75, 360, mode="G0", feedrate=speedRobot) #move coaster into presser station
dexarmPicker.air_picker_stop()
dexarmPicker.move_to(13, 238, -75, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarmPicker.move_to(13, 238, -85, 360, mode="G0", feedrate=speedRobot) #put arm into position to push
dexarmPicker.move_to(13, 300, -85, 360, mode="G0", feedrate=speedRobot) #push coaster into presser station
dexarmPicker.move_to(13, 238, -85, 360, mode="G0", feedrate=speedRobot) #move arm back
dexarmPicker.move_to(13, 223, -9, 360, mode="G1", feedrate=speedRobot) #move arm up
dexarmPicker.move_to(13, 222, -9, 360, wait = True) #move arm up
dexarmPicker.move_to(13, 220, -9, 360, wait = True) #move arm up
p_f.PressureStationGo()

dexarmPicker.move_to(-1, 283, -70, 360, mode="G0", feedrate=speedRobot) #move arm above pick up area
dexarmPicker.move_to(-1, 283, -90, 360, mode="G0", feedrate=speedRobot) #move arm down to pick up coaster
dexarmPicker.air_picker_pick() #pick up coaster
dexarmPicker.move_to(-1, 260, -90, 360, mode="G0", feedrate=speedRobot) #move arm out with coaster 
dexarmPicker.move_to(-4, 228, -30, 360, mode="G0", feedrate=speedRobot) #move arm up
'''

"""
grabCoaster(dexarmPicker) #Grab a coaster... then do stuff with it

flipCoaster(dexarmPicker) #Call the module that flips the coaster. 

#if this works, drop it off

drop_coaster(dexarmPicker)

#Let's place some fuzzy feet. 
pick_indices = [(1, 1), (2, 1), (3, 1)] #Pick the first, second, and third foor in the first row 

placeFuzzyFeet(dexarmAdhesive,pick_indices,3)
"""