import pressure_flipper_serial as p_f
import laser_module as l_m
import time
import keyboard
import sys

l_m.initializeArduino()
p_f.initializePressureFlipperArduino()


while True:
    keyboard.read_key()

    if keyboard.is_pressed('p'): # press 'p' key to start Pressure Sequence
        p_f.PressureStationGo()

    if keyboard.is_pressed('f'): # press 'f' key to start Flipper Sequence
        p_f.FlipperStationGo()
    
    if keyboard.is_pressed('o'): # press 'o' to open laser door
        l_m.LaserDoorOpen()

    if keyboard.is_pressed('c'): # press 'c' to close laser door
        l_m.LaserDoorClose()

    # Exit Program
    if keyboard.is_pressed('ESC'):
        sys.exit()