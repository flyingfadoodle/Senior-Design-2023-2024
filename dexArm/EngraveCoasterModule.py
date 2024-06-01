from pydexarm import Dexarm #Get the main dexarm class. 

#Get the modules we need to initialize the laser, flipper, and pressure stations. 
import laser_module as l_m
import time #In case we need it. 

#Lower-level modules
from laserModule import laserDropOff, laserPickUp

speedRobot = 6000 #Feedrate

def get_filename(coasterVariant):
    file_map = { #Define an index of the GCODE files we need to use. For now, these are placeholders. 
        1: "outputGcode1.txt",
        2: "outputGcode2.txt",
        3: "outputGcode3.txt",
        4: "outputGcode4.txt"
    }
    if coasterVariant in file_map:
        return file_map[coasterVariant]
    else:
        raise RuntimeError(f"No filename available for coasterVariant index {coasterVariant}. Stopping execution. ")

def EngraveCoaster(dexarmPicker,dexarmLaser,coasterVariant): #Decalre coasterVariant as an int, from 1 to N
    

    dexarmPicker.move_to(0,240,0,880,mode="G0",feedrate=speedRobot) #Make sure that the arm is out of the way. 

    #Begin laser module

    #Open the door
    l_m.LaserDoorOpen() #We're assuming the microcode gets fixed so that the door consistently opens and consistently closes. 
    
    #Drop off coaster inside of 
    laserDropOff(dexarmPicker, dexarmLaser) #TODO: Modify this module to use relative coordinates for sanity reasons. 
  
    #Close the door
    l_m.LaserDoorClose() #Also assuming the door closes coorectly. 



    #NOTE: We are also assuming that the box closes correctly before running. 



    #TODO: ADD INTERLOCK. 

    #Use the filename mapping function defined previous to grab the correct filename from a list. 
    fileName = get_filename(coasterVariant)
    print("Currently attempting to engrave " + fileName) #I love Python's mixed expression syntax. Makes so much sense. 

    #l_m.runLaser(dexarmLaser, fileName) 
    print("Laser would be running here, except Alex doesn't trust the box to close properly.")
    time.sleep(5) #Wait 5 seconds. Purely for debug, NOTE: Remove this once you un-comment out the actual runLaser line. 

    #Open the box again when finished. 
    l_m.LaserDoorOpen()
    
    #Grab the coaster from the laser box, then continue with your business. 
    laserPickUp(dexarmPicker, dexarmLaser)
    #END LASER MODULE
    







