from pydexarm import Dexarm
import pydexarmCustom
import laser_module as l_m
import pressure_flipper_serial as p_f
import sys
sys.path.insert(0, 'LaserModule')
sys.path.insert(0, "MovementModule")

#Define Dexarm objects
dexarmPicker = Dexarm(port="COM19") #COM port for Picker ARM
#dexarmAdhesive = Dexarm(port="COM4") #COM port for Adhesive ARM 
#dexarmLaser = Dexarm(port="COM6") #COM port for laser ARM

#Variables related to laser
coasterDesign = 1 #Which coaster variant are we doing
loops = 1 #loops wanted

#MAIN BODY OF CODE
fuzzyX = 205 #In theory, I can just change this to a 200- equal in magnitude to the amount we moved to the side. 
fuzzyY_hover = 240
fuzzyY_insert = fuzzyY_hover + 80 #should equal 300 for current config. This is like this in case we move the jig forwards or backwards.
fuzzyZ = -88
RAIL_FUZZY_COASTER_JIG = 680
speedRobot = 6000

p_f.initializePressureFlipperArduino() #Initialize flipper module Arduino
dexarmPicker.sliding_rail_init()
dexarmPicker.go_home()

dexarmPicker.move_to(fuzzyX, fuzzyY_insert-5, fuzzyZ + 10, RAIL_FUZZY_COASTER_JIG, mode="G0", feedrate=speedRobot) #Move to hover above pickup spot NOTE: The +10 is to compensate for the coaster being pushed inwards. 
dexarmPicker.move_to(fuzzyX, fuzzyY_insert-5, fuzzyZ, mode="G1", feedrate=speedRobot) #Go down, slowly. 
dexarmPicker.air_picker_pick() #Grab coaster
dexarmPicker.move_to(fuzzyX, fuzzyY_hover, fuzzyZ, mode="G1", feedrate=speedRobot) #Move backwards prior to going up, to clear jig
dexarmPicker.move_to(fuzzyX, fuzzyY_hover, 0, mode="G0", feedrate=speedRobot) #Move upwards- at a diagonal to clear the screw. 

pydexarmCustom.pressCoaster(dexarmPicker)
 
pydexarmCustom.deposit_coaster(dexarmPicker)