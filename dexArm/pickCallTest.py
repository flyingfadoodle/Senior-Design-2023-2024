# Base code by Samuel Lim
# Modified by Alenxader Torres on 4.24.24
# Additions with the help of Chat GPT 4.0 Turbo 
#This code uses spaces and not tabs. I apolgize in advance. 

import sys
import time
from pydexarm import Dexarm


# Add Movement module
sys.path.insert(0, "MovementModule")


# Constants
SPEED_ROBOT = 4000  # Original 6000
SPEED2_ROBOT = 100  # Lower speed for fine motions
PICK_X = -50
PICK_Y = 229
PICK_Z = -88
OFFSET_Z = 8;  # Offset to go down and pick
OFFSET_2 = 1  # Offset when sliding forwards when picking
FOOT_SPACING_X = 24.5  # Distance between the center of feet, in mm
FOOT_SPACING_Y = 23.66 

# Initialization
dexarm2 = Dexarm(port="COM4")
dexarm2.go_home()


def robotPrintLocation(): #imported from other functions
    dexarm2._send_cmd("G92.1\r");#Resets
    x,y,z,e,_,_,_ =dexarm2.get_current_position()
    print(x,y,z,e, "mm")


def pick_fuzzy_foot(dexarm, index_x, index_y):
    
	# Calculate target coordinates based on index
	target_x = PICK_X + (index_x - 1) * FOOT_SPACING_X
	target_y = PICK_Y + (index_y - 1) * FOOT_SPACING_Y
	dexarm.go_home() #At the start of each pick, go home.


	# Hover above the target position
	dexarm.move_to(target_x, target_y, 0, mode="G1", feedrate=SPEED_ROBOT)
	robotPrintLocation() #debug to output where we are 
	# Drop down to just above the pick position
	dexarm.move_to(target_x, target_y, PICK_Z, mode="G1", feedrate=SPEED_ROBOT)
	# Move down slowly to grab the fuzzy foot
	dexarm.move_to(target_x, target_y, PICK_Z - OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT)
	# Slide forwards slowly to ensure grip
	dexarm.move_to(target_x, target_y + OFFSET_2, PICK_Z - OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT/2) #Halve speedrobot for good measure. This is a small move. 
	# Begin lifting the foot
	dexarm.move_to(target_x, target_y + OFFSET_2, PICK_Z, mode="G1", feedrate=SPEED2_ROBOT)
	# Lift up completely
	dexarm.move_to(target_x, target_y + OFFSET_2, 0, mode="G1", feedrate=SPEED_ROBOT)
	# Finish sequence
	print(f"Attempted pick at [{index_x}, {index_y}] -")
	dexarm.go_home() #Home at the end of the sequence for a consistent starting point. 
   



# Example usage: Picking the fuzzy foot at index [X,Y]
#pick_fuzzy_foot(dexarm2, 5, 5)





#placeFuzzyFeet begins here

import math

# Constants
PLACEMENT_RADIUS = 70 / math.sqrt(3)  # Radius for equilateral triangle placement
TRIANGLE_ANGLE = math.radians(60)  # 60 degrees for equilateral triangle
COASTER_X = -217
COASTER_Y = 171
HOVER_Z = -82
PLACEMENT_OFFSET_Z = 8; 

def calculate_triangle_positions():
    # Calculate positions of the triangle points around the center
    positions = []
    for i in range(3):
        angle = TRIANGLE_ANGLE * i - math.pi / 2  # Adjusting for "upside down" triangle
        x = COASTER_X + PLACEMENT_RADIUS * math.cos(angle)
        y = COASTER_Y + PLACEMENT_RADIUS * math.sin(angle)
        positions.append((x, y))
    return positions

def placeFuzzyFeet(dexarm, pick_indices, num_to_place):
    # Ensure valid number of placements
    if not 1 <= num_to_place <= 3:
        print("Invalid number of feet to place. Please choose between 1 and 3.")
        return

    # Get triangle positions
    positions = calculate_triangle_positions()

    # Loop through the specified number of fuzzy feet to place
    for i in range(num_to_place):
        idx_x, idx_y = pick_indices[i]
        pick_fuzzy_foot(dexarm, idx_x, idx_y)  # Pick the fuzzy foot
        placement_x, placement_y = positions[i]
        #Do NOT call PickZ, it corresponds to the fuzzy feet plate, which has a different height. 
        # Move to placement position
        dexarm.move_to(placement_x, placement_y, 0, mode="G1", feedrate=SPEED_ROBOT)
        # Move down most of the way
        dexarm.move_to(placement_x, placement_y, HOVER_Z, mode="G1", feedrate=SPEED_ROBOT)
        # Move the rest of the way, slowly
        dexarm.move_to(placement_x, placement_y, HOVER_Z - PLACEMENT_OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT)
        # Move back up, slowly
        dexarm.move_to(placement_x, placement_y, HOVER_Z, mode="G1", feedrate=SPEED2_ROBOT)
        # Move the rest of the way up to Z=0
        dexarm.move_to(placement_x, placement_y, 0, mode="G1", feedrate=SPEED_ROBOT)
        print(f"Placed fuzzy foot {i+1} at [{placement_x}, {placement_y}]")

# Example usage
pick_indices = [(1, 1), (2, 1), (3, 1)]
placeFuzzyFeet(dexarm2, pick_indices, 3)

