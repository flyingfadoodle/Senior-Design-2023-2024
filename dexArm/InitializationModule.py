"""This function re-sets the Workcell and initializes all the stations, in-order. 

NOTE: All parameters here are hardcoded. For example, if a COM port changes, update it here. """

from pydexarm import Dexarm #Get the main dexarm class. 

#Get the modules we need to initialize the laser, flipper, and pressure stations. 
import laser_module as l_m
import pressure_flipper_serial as p_f
import time


speedRobot = 6000 #Keeping this, since the initialization process has some travel moves. 


def initializeWorkcell(dexarmPicker, dexarmAdhesive, dexarmLaser):
   """Initializes the workcell. Takes in three dexarm objects- corresponding to the picker station, adhesive station, and laser box, in that order.
    
     NOTE: This whole  """
   # INITIALIZATION
   l_m.initializeArduino() #Initialize laser module arduino 
   p_f.initializePressureFlipperArduino() #Initialize flipper module Arduino

   #Homing sequence
   dexarmAdhesive.go_home() #First, home the Adhesive station arm.
   dexarmAdhesive.move_to(-200, 30, 0, mode="G0", feedrate=speedRobot) #Then, make sure the adhesive arm moves out of the way. 
   time.sleep(5) #Wait 5 seconds before moving the main picker. 

   #The Picker goes home next. 
   dexarmPicker.go_home() #Goes to robot home position
   
   #Initialize the sliding rail. This way, we can make sure the door is closed prior to starting anything. 
   dexarmPicker.sliding_rail_init()
   robotConnectedRail = True

   #Move the picker arm, with the sliding rail, to the loading position. We are assuming this will be a common start point. Plus, we clear the laser door. 
   dexarmPicker.move_to(220, 57, 120, 880, mode="G0", feedrate =speedRobot) #We're moving to the exact loading position, used in PickerLoadingModule.py

   #Home the laser arm. 
   dexarmLaser.go_home()

   #Lastly. make sure that the laser door is closed. 
   l_m.LaserDoorClose()
   #TODO: Add interlock to throw an error if the door doesn't close correctly. Can probably piggyback of the Servo Arduino. 

def goHomes(dexarmPicker, dexarmAdhesive, dexarmLaser):
   "Tells the givne dexarm objects to go to their home points."
   dexarmPicker.go_home()
   dexarmAdhesive.go_home()
   dexarmLaser.go_home()



