#Add Laser Module:
import sys
sys.path.insert(0, 'LaserModule')
import laser_module as l_m

import time
import keyboard
#plug the arduino module into the PC
#press the play button in the top right to run the program

l_m.initializeArduino() 
#if there is a conection failure, refer to line 204 in the "laser_module.py" file and change the COM port to the appropriate number

#Where is the locator for the pins on the arduino? 
while True:
    keyboard.read_key()

    if keyboard.is_pressed('o'): #press the 'o' key to OPEN the laser door
       l_m.LaserDoorOpen()

    if keyboard.is_pressed('c'): #press thye 'c' key to CLOSE the laser door
        l_m.LaserDoorClose()

    #Exit Program:oocc
    if keyboard.is_pressed('ESC'):
        sys.exit()

#if you get other errors in the terminal press ctrl-c or ctrl-d to terminate the program