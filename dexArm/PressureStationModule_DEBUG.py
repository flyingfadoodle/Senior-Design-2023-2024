# Generated by ChatGPT 4.0 on April 29, 2024.
# Modified by Alexander Torres on 4.30.24 to fix syntax errors and improve readability.
# Additional comments by Alexander Torres and ChatGPT 4.0.

"""
This module automates the process of applying pressure to a coaster using a robotic arm
equipped with a pressure station. It includes moving the coaster into position, activating
the pressure mechanism, and retrieving the coaster after the operation.

Function:
- pressCoaster(dexarm): Controls the robotic arm to press a coaster and retrieve it post-process.
"""

from pydexarm import Dexarm
from PickVerificationModule import pickStatus  # Assuming this is the correct module name
import pressure_flipper_serial as p_f  # Existing module for flipper station functionality

# Constants for movement
pressure_X = 13
hover_Y = 240 #Seems like 220 just don't work? edit: yeah setting this to 220 causes XY limit errors. I wish I knew what the actual XY limits were, lol
pressure_Z = -80
hover_Z = pressure_Z + 60
insert_Y = hover_Y + 50
push_Y = 238
pickup_X = -1 #Why is this different? 
pickup_Z = -90
RAIL_PRESSURE_POS = 360  # Constant where the rail parks when using the pressure station
speedRobot = 6000  # Feedrate for robot movements

def pressCoaster(dexarm):
    """
    Moves the assigned dexarm to the pressure station and loads, pushes, presses, and unload a coaster.

    Parameters:
    - dexarm: Instance of Dexarm object. Should be our picker.
    """
    #Hover above pressure station. 
    dexarm.move_to(pressure_X, hover_Y, hover_Z, RAIL_PRESSURE_POS, mode="G0", feedrate=speedRobot)
   
    #Move to drop-off point
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G1", feedrate=speedRobot)

    #Move forwards, then drop the coaster
    dexarm.move_to(pressure_X, insert_Y, pressure_Z, mode="G1", feedrate=speedRobot)
    dexarm.air_picker_stop()

    #Push sequence for inserting fully into pressure station
    dexarm.move_to(pressure_X, hover_Y, pressure_Z + 10, mode="G1", feedrate=speedRobot) #Back while 10mm above final pressure height
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G1", feedrate=speedRobot) #Move down 
    dexarm.move_to(pressure_X, insert_Y, pressure_Z, mode="G1", feedrate=speedRobot) #Push forwards

    #Go back once you're done pushing
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G1", feedrate=speedRobot) #move back
    dexarm.move_to(pressure_X, hover_Y, pressure_Z + 10, mode="G1", feedrate=speedRobot) #Move up a wee bit for good measure. 

    #Activate pressure station. Again, this assumes it's initalized already in our main initialization function. 
    p_f.PressureStationGo()

    #Grab the coaster from the station
    dexarm.move_to(pickup_X, insert_Y, pressure_Z + 10, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pickup_X, insert_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.air_picker_pick()
    dexarm.move_to(pickup_X, hover_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pickup_X, hover_Y, hover_Z, mode="G0", feedrate=speedRobot)

    #Check if we picked the coaster correctly. Otherwise, throw an error and break. 
    if not pickStatus():
        print("Pick at picker station failed! Did the coaster end up somewhere unexpected? Returning False..")
        return False
    

    print("Pressure operation completed successfully.")
    return True

# Optional testing block
if __name__ == "__main__":

    #to make this test work correctly 
    p_f.initializePressureFlipperArduino()
    dexarm = Dexarm(port='COM19')
    success = pressCoaster(dexarm)
    print("Operation success:", success)



