import sys, math, time, serial
from pydexarm import Dexarm

SPEED_ROBOT = 6000
speedRobot = 6000

def get_sensor_height():
    SERIAL_PORT = 'COM24'
    BAUD_RATE = 115200
    TIMEOUT = 1
    CALIBRATION_OFFSET = 40.0

    serial_connection = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
    time.sleep(2)  # Allow time for the serial connection to establish
    print("Serial connection established with TOF Sensor on", SERIAL_PORT)

    # Command the Arduino to start measurement
    serial_connection.write(b"$M\n")
    raw_measurement = None

    # Wait for and process the incoming data
    while True:
        if serial_connection.in_waiting > 0:
            line = serial_connection.readline().decode().strip()
            if line.startswith("$M"):
                # Parse the average distance measurement
                raw_measurement = float(line[2:])
            elif line == "$D":
                # End of measurement data transmission
                break

    if raw_measurement is None:
        print("Measurement error or no data received.")
        return None

    # Apply the calibration offset and round the result
    calibrated_measurement = round(raw_measurement - CALIBRATION_OFFSET, 1)

    # Debug message
    print(f"Debug Info: Raw measurement = {raw_measurement} mm, "
          f"Calibrated measurement = {calibrated_measurement} mm, "
          f"Current offset = {CALIBRATION_OFFSET} mm")

    serial_connection.close()
    print("Serial connection closed with TOF Sensor.")
    return calibrated_measurement

def pickStatus():
    sensor_threshold = 10
    measured_height = get_sensor_height()
    
    if measured_height < sensor_threshold:
        return True
    else:
        print(f"Sensor reading is {measured_height}mm - above missed pick threshold of {sensor_threshold}mm. Returning False.")
        return False
    
def stopWorkcell(dexarm):
   dexarm.air_picker_stop()

def initialize_picker_arm(dexarm):
    dexarm.sliding_rail_init()
    print("Sliding rail initialized and connected.")

def grabCoaster(dexarm):
        RAIL_SOUTH_POS = 880
        loading_X = 320 #changed from 316 to 320
        loading_Y = 57 #changed from 54 to 57
        loading_hover_Z = 120
        #speedRobot = 6000
        slow_feedrate = 1000  # Slower feedrate for the final precise movement
        loading_clearance_X = 100
        # Move to a clearance position before going directly above the coaster
        dexarm.move_to(loading_X - loading_clearance_X, loading_Y, loading_hover_Z, RAIL_SOUTH_POS, mode="G0", feedrate=speedRobot)

        # Move to the hover position above the coaster stack
        dexarm.move_to(loading_X, loading_Y, loading_hover_Z, RAIL_SOUTH_POS, mode="G1", feedrate=speedRobot)

        # Take a sensor reading
        height = get_sensor_height()
        print(f"Sensor height measurement: {height} mm")

        # Move quickly to 10 mm above the target Z
        target_Z_quick = loading_hover_Z - height + 10
        dexarm.move_to(loading_X, loading_Y, target_Z_quick, RAIL_SOUTH_POS, mode="G1", feedrate=speedRobot)

        # Move slowly for the last 10 mm
        target_Z_slow = loading_hover_Z - height
        dexarm.move_to(loading_X, loading_Y, target_Z_slow, RAIL_SOUTH_POS, mode="G1", feedrate=slow_feedrate)

        # Initialize the vacuum picker
        dexarm.air_picker_pick()

        # Lift back up at normal speed
        dexarm.move_to(loading_X, loading_Y, target_Z_slow+20, RAIL_SOUTH_POS, mode="G1", feedrate=speedRobot) #Lift straight up first otherwise the non-edge-filleted coasters stick together. 

        # Lift back up at normal speed
        dexarm.move_to(loading_X - loading_clearance_X, loading_Y, loading_hover_Z, RAIL_SOUTH_POS, mode="G1", feedrate=speedRobot)

        if not pickStatus():
        #This throws a runtime error if the sensor check fails. For more robust error handling, change this back to a "print" and instead return false. 
           stopWorkcell(dexarm)
           raise RuntimeError("Pick at loading area failed! Are we out of coasters? Stopping execution.")

def deposit_coaster(dexarm):
    unloading_X = 295
    unloading_Y = 234
    unloading_Z = 60
    RAIL_SOUTH_POS = 880  # Position of the sliding rail
    #speedRobot = 6000
    
    #Move to the unloading position with reduced X for better clearance
    dexarm.move_to(unloading_X-100, unloading_Y, unloading_Z, RAIL_SOUTH_POS, mode="G0", feedrate=speedRobot)
    
    #Move to the unloading position
    dexarm.move_to(unloading_X, unloading_Y, unloading_Z, RAIL_SOUTH_POS, mode="G0", feedrate=speedRobot)
    
    #Release the coaster
    dexarm.air_picker_stop()
    
    #Retract to clear the drop-off area
    dexarm.move_to(unloading_X, unloading_Y, unloading_Z + 10, RAIL_SOUTH_POS, mode="G1", feedrate=speedRobot)

def robotPrintLocation(dexarm): #copy pasted for debugging 
    dexarm._send_cmd("G92.1\r")
    x, y, z, e, _, _, _ = dexarm.get_current_position()
    print(x, y, z, e, "mm")

def assign_pick_indices(loops):
   if loops == 1:
       pick_indices = [(1, 1), (2, 1), (3, 1)]
   elif loops == 2:
       pick_indices = [(4, 1), (5, 1), (5, 2)]
   elif loops == 3:
       pick_indices = [(5, 3), (5, 4), (5, 5)]
   elif loops == 4:
       pick_indices = [(4, 5), (3, 5), (2, 5)]
   else:
       raise ValueError("Invalid value for 'loops'. Must be between 1 and 4.")

   return pick_indices

def pick_fuzzy_foot(dexarm, index_x, index_y):

    "You've become the very thing you swore to destroy- hardcoded constants. "
    SPEED2_ROBOT = 100
    PICK_Z = -88  # The height to pick the fuzzy feet, adjusted for the actual height of the coaster
    OFFSET_Z = 8; 
    
    # Hardcoded positions for each index in the 5x5 array

    #NOTE: y'know, maybe just skip 1,2. it refuses to work and is a stubborn fuzzy foot
    #3,4 is also a problem
    #...and 4,4
    #...and
    #(you left off at - , 4,2, 3,2, and 3,3 are left)
    predefined_positions = {
        (1, 1): (-51, 228), (1, 2): (-27+2, 228), (1, 3): (0, 228+1), (1, 4): (27-2, 228+1), (1, 5): (51, 228+1),
        (2, 1): (-51, 252), (2, 2): (-27+2, 252), (2, 3): (0, 252), (2, 4): (27-1, 252+1), (2, 5): (51, 252+1),
        (3, 1): (-51, 276), (3, 2): (-27+1, 276), (3, 3): (-1, 276), (3, 4): (27-2, 276), (3, 5): (51-1, 276+1),
        (4, 1): (-51, 300), (4, 2): (-27+2, 300), (4, 3): (0, 300), (4, 4): (27-2, 300+2), (4, 5): (51-2, 300+1),
        (5, 1): (-51+1, 324-1), (5, 2): (-27+1, 324), (5, 3): (-1, 324), (5, 4): (27-3, 324+1), (5, 5): (51-2, 324+1),
    }

    # Get the target position from the predefined positions
    target_x, target_y = predefined_positions.get((index_x, index_y), (None, None))

    dexarm.go_home()
    dexarm.move_to(target_x, target_y, 0, mode="G0", feedrate=SPEED_ROBOT) #Move to desired position, with Z=0
    robotPrintLocation(dexarm)
    dexarm.move_to(target_x, target_y, PICK_Z, mode="G0", feedrate=SPEED_ROBOT) #Descend to hover height 
    dexarm.move_to(target_x, target_y, PICK_Z - OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT) #Drop down to pick, with reduced speed
    dexarm.move_to(target_x, target_y, PICK_Z - OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT/2) #Slide forwards to ensure grab - reduced speed
    dexarm.move_to(target_x, target_y, PICK_Z, mode="G1", feedrate=SPEED2_ROBOT) #Begin to raise picker - reduced speed
    dexarm.move_to(target_x, target_y, 0, mode="G0", feedrate=SPEED_ROBOT) #Ascend back to Z = 0
    print(f"Attempted pick at [{index_x}, {index_y}]") #debug

def calculate_triangle_positions():
    #Constants for FEET PLACEMENT
    PLACEMENT_RADIUS = 70 / math.sqrt(3) #Change the "70"(mm) to something else if the coaster size changes. 
    TRIANGLE_ANGLE = math.radians(120) #Angle between fuzzy feet

    #The following two variables are the constant X, Y, Z center for the coaster having feet placed on it. 
    COASTER_X = -217
    COASTER_Y = 171

    positions = []
    for i in range(3): #Figure out where to put the three coaster feet, using the desired (70mm) distance. 
        angle = TRIANGLE_ANGLE * i - math.pi/2
        x = COASTER_X + PLACEMENT_RADIUS * math.cos(angle)
        y = COASTER_Y + PLACEMENT_RADIUS * math.sin(angle)
        positions.append((x, y))
    return positions

def placeFuzzyFeet(dexarm, pick_indices, num_to_place):
    #SPEED_ROBOT = 6000
    SPEED2_ROBOT = 100
    HOVER_Z = -84 #Actual height of arm against coaster is 90mm. 84+6 = 90mm. 
    PLACEMENT_OFFSET_Z = 6

    if not 1 <= num_to_place <= 3:
        print("Invalid number of feet to place. Please choose between 1 and 3.") #num_to_place exists only for debugging, so you can place only one foot at a time. Under normal circumstances, always feed it 3. 
        return
    positions = calculate_triangle_positions()
    for i in range(num_to_place):
        idx_x, idx_y = pick_indices[i] #Grab our desired pick positions as integers, so [2,1] get passed into two variables as idx_x = 2 and idx_y = 1
        pick_fuzzy_foot(dexarm, idx_x, idx_y) #Call the previous function to grab the fuzzy foot at the desired position. 
        placement_x, placement_y = positions[i] #Get our foot placement positions
        dexarm.move_to(placement_x, placement_y, 0, mode="G0", feedrate=SPEED_ROBOT) #Go to desired pos @ Z=0
        dexarm.move_to(placement_x, placement_y, HOVER_Z, mode="G0", feedrate=SPEED_ROBOT) #Go to hover height
        dexarm.move_to(placement_x, placement_y, HOVER_Z - PLACEMENT_OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT*2) #Go down, slightly less slowly to place 
        dexarm.move_to(placement_x, placement_y, HOVER_Z + PLACEMENT_OFFSET_Z, mode="G1", feedrate=SPEED2_ROBOT*2) #Go up, less slowly
        dexarm.move_to(placement_x, placement_y, 0, mode="G0", feedrate=SPEED_ROBOT) #Return to Z=0
        print(f"Placed fuzzy foot {i+1} at [{placement_x}, {placement_y}]") #debug

def flipCoaster(dexarm):
    import pressure_flipper_serial as p_f 
    idle_X = 0
    idle_Y = 200
    idle_Z = 0
    RAIL_NORTH_POS = 0
    dropoff_X = -61
    dropoff_Y = 342
    dropoff_Z = -65
    pickup_X = 50
    pickup_Y = 347
    pickup_Z = -93
    #speedRobot = 6000  # feedrate for robot movements

    dexarm.go_home() #Go home, to try and fix the error these three lines are throwing. 
    dexarm.move_to(idle_X, idle_Y, idle_Z, RAIL_NORTH_POS, mode="G0", feedrate=speedRobot) #Move to a safe idle position

    # Move to slightly above dropoff position
    dexarm.move_to(dropoff_X, dropoff_Y, dropoff_Z+20, mode="G0", feedrate=speedRobot)
    # Move to the dropoff position itself
    dexarm.move_to(dropoff_X, dropoff_Y, dropoff_Z, mode="G1", feedrate=speedRobot)
    
    dexarm.air_picker_stop()  # Release coaster at the flip station
    
    # Return to idle to initiate flipping
    dexarm.move_to(idle_X, idle_Y, idle_Z, mode="G0", feedrate=speedRobot)
    time.sleep(3) #Wait 3 seconds to let arm clear. Not sure why this broke but it did. 

    # Activate the flipper via Arduino
    p_f.FlipperStationGo()

    # Move to SLIGHTLY ABOVE pickup position and retrieve the flipped coaster
    dexarm.move_to(pickup_X, pickup_Y, pickup_Z+20, mode="G0", feedrate=speedRobot)
    #Move to the actual pikcup position 
    dexarm.move_to(pickup_X, pickup_Y, pickup_Z, mode="G1", feedrate=speedRobot)
    dexarm.air_picker_pick()  # Engage picker to grab the coaster

    # Raise the coaster to clear the flipper table
    dexarm.move_to(pickup_X, pickup_Y, pickup_Z + 40,mode="G0", feedrate=speedRobot)

    if not pickStatus():
        #This throws a runtime error if the sensor check fails. For more robust error handling, change this back to a "print" and instead return false. 
        stopWorkcell(dexarm) 
        raise RuntimeError("Pick at picker station failed! Did the coaster end up somewhere unexpected? Stopping execution.")
        #return false #This will be more useful for more robust error handling. For now, the code just stops. 

    # Move back to the idle position to complete the cycle
    dexarm.move_to(idle_X, idle_Y, idle_Z, RAIL_NORTH_POS, mode="G0", feedrate=speedRobot)

def pressCoaster(dexarm):
    import pressure_flipper_serial as p_f
    pressure_X = 13
    hover_Y = 240
    pressure_Z = -80
    hover_Z = pressure_Z + 60
    insert_Y = hover_Y + 50
    #Removed pickup_X since it's identical to pressure_X
    RAIL_PRESSURE_POS = 360  # Constant where the rail parks when using the pressure station
    #speedRobot = 6000  # Feedrate for robot movements

    dexarm.move_to(pressure_X, hover_Y, hover_Z, RAIL_PRESSURE_POS, mode="G0", feedrate=speedRobot) #Hover above pressure station. 
   
    #Move own to dropoff point. 
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G1", feedrate=speedRobot)

    #Move forwards, then drop the coaster
    dexarm.move_to(pressure_X, insert_Y, pressure_Z, mode="G1", feedrate=speedRobot)
    dexarm.air_picker_stop()

    #Move straight up before moving back, to not accidentally drag the coaster backwards 
    dexarm.move_to(pressure_X, insert_Y, pressure_Z + 10, mode="G1", feedrate=speedRobot) #Move to 10mm straight up to be consistent with the next move and avoid unwanted pushing. 

    #Push sequence for inserting fully into pressure station
    dexarm.move_to(pressure_X, hover_Y-10, pressure_Z + 10, mode="G1", feedrate=speedRobot) #Back while 10mm above final pressure height. Also 10mm extra back to avoid clipping. 
    dexarm.move_to(pressure_X, hover_Y-10, pressure_Z - 5, mode="G1", feedrate=speedRobot) #Move down -5mm to bump into the coaster properly
    dexarm.move_to(pressure_X, insert_Y, pressure_Z - 5, mode="G1", feedrate=speedRobot) #Push forwards

    #Go back once you're done pushing
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G1", feedrate=speedRobot) #This moves slightly diagonal but it should be O-K.
    dexarm.move_to(pressure_X, hover_Y, pressure_Z + 10, mode="G1", feedrate=speedRobot) #Move up a wee bit for good measure. 

    #Activate pressure station. Again, this assumes it's initalized already in our main initialization function. 
    p_f.PressureStationGo()

    #Grab the coaster from the station
    dexarm.move_to(pressure_X, insert_Y, pressure_Z + 10, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pressure_X, insert_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.air_picker_pick()

    #Pull coaster backwards into alignment jig
    dexarm.move_to(pressure_X, hover_Y-10, pressure_Z-5, mode="G0", feedrate=speedRobot)
    dexarm.air_picker_stop()

    #Pick it up again, now that it's aligned
    dexarm.move_to(pressure_X, hover_Y, pressure_Z+10, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pressure_X, hover_Y+15, pressure_Z-5, mode="G0", feedrate=speedRobot)
    dexarm.air_picker_pick()

    dexarm.move_to(pressure_X, hover_Y+15, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pressure_X, hover_Y+15, hover_Z, mode="G0", feedrate=speedRobot)
    """
    #THIS IS THE OLD CODE, IN CASE SOMETHING BREAKS 
    dexarm.move_to(pressure_X, insert_Y, pressure_Z + 10, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pressure_X, insert_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.air_picker_pick()

    #Pull coaster backwards into alignment jig
    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.air_picker.stop()

    dexarm.move_to(pressure_X, hover_Y, pressure_Z, mode="G0", feedrate=speedRobot)
    dexarm.move_to(pressure_X, hover_Y, hover_Z, mode="G0", feedrate=speedRobot)
    """
    #Check if we picked the coaster correctly. Otherwise, throw an error and break. 
    if not pickStatus():
        #This throws a runtime error if the sensor check fails. For more robust error handling, change this back to a "print" and instead return false. 
        stopWorkcell(dexarm)
        raise RuntimeError("Final pick at pressure station failed! Did the coaster end up somewhere unexpected?")
        #return false #This will be more useful for more robust error handling. For now, the code just stops. 

    print("Pressure operation completed successfully.")

def applyFuzzyFeet(dexarmPicker, dexarmAdhesive, pick_indices):
    fuzzyX = 205 #In theory, I can just change this to a 200- equal in magnitude to the amount we moved to the side. 
    fuzzyY_hover = 240
    fuzzyY_insert = fuzzyY_hover + 80 #should equal 300 for current config. This is like this in case we move the jig forwards or backwards.
    fuzzyZ = -88
    RAIL_FUZZY_COASTER_JIG = 680 #Moved 200mm to the side as our current orientation is bad. Original was 880. 
    #speedRobot = 6000
    dexarmPicker.go_home() #Make sure arm is home'd correctly, prior to continuing. 

    dexarmPicker.move_to(fuzzyX, fuzzyY_hover, 0, RAIL_FUZZY_COASTER_JIG, mode="G0", feedrate=speedRobot)
    dexarmPicker.move_to(fuzzyX, fuzzyY_hover, fuzzyZ, mode="G0", feedrate=speedRobot) #Move down to the correct height to insert
    dexarmPicker.move_to(fuzzyX, fuzzyY_insert, fuzzyZ, mode="G1", feedrate=speedRobot) #Move forward to insert
    dexarmPicker.air_picker_stop()  # Release coaster inside of jig
    dexarmPicker.move_to(fuzzyX, fuzzyY_insert, fuzzyZ + 30, mode="G1", feedrate=speedRobot)  # Raise slightly prior to moving to wait position (not to be confused with idle)
    dexarmPicker.move_to(240, 50, 0, mode="G0", feedrate=speedRobot) #Move picker out of the way. 

    placeFuzzyFeet(dexarmAdhesive, pick_indices, 3)
       
    dexarmAdhesive.move_to(-200, 30, 0, mode="G1", feedrate=speedRobot) #Move adhesive picker arm out of the way

        # Pickup the coaster after fuzzy feet application
    dexarmPicker.move_to(fuzzyX, fuzzyY_insert-5, fuzzyZ + 10, mode="G0", feedrate=speedRobot) #Move to hover above pickup spot NOTE: The +10 is to compensate for the coaster being pushed inwards. 
    dexarmPicker.move_to(fuzzyX, fuzzyY_insert-5, fuzzyZ, mode="G1", feedrate=speedRobot) #Go down, slowly. 
    dexarmPicker.air_picker_pick() #Grab coaster
    dexarmPicker.move_to(fuzzyX, fuzzyY_hover, fuzzyZ, mode="G1", feedrate=speedRobot) #Move backwards prior to going up, to clear jig
    dexarmPicker.move_to(fuzzyX, fuzzyY_hover, 0, mode="G0", feedrate=speedRobot) #Move upwards- at a diagonal to clear the screw.         

        # Sensor check to confirm pickup
    if not pickStatus():
        stopWorkcell(dexarmPicker)
        raise RuntimeError("Final pick at adhesive station failed! Did the coaster get stuck?")
        #If nothing goes wrong, print as such to console. 
    print("Adhesive operation completed successfully. (As far as picking goes)")

def initializeWorkcell(dexarmPicker, dexarmAdhesive, dexarmLaser):
    import laser_module as l_m
    import pressure_flipper_serial as p_f
    #speedRobot = 6000

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
    #robotConnectedRail = True

   #Move the picker arm, with the sliding rail, to the loading position. We are assuming this will be a common start point. Plus, we clear the laser door. 
    dexarmPicker.move_to(220, 57, 120, 880, mode="G0", feedrate =speedRobot)
    dexarmLaser.go_home()

   #Lastly. make sure that the laser door is closed. 
    l_m.LaserDoorClose() 

def goHomes(dexarmPicker, dexarmAdhesive, dexarmLaser):
    dexarmPicker.go_home()
    dexarmAdhesive.go_home()
    dexarmLaser.go_home()

def laserDropOff(dexarmPicker, dexarmLaser):
    #speedRobot = 6000
    dexarmLaser.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot) #move laser dexarm up
    dexarmPicker.move_to(0, 200, 0, 350, mode="G0", feedrate=speedRobot) #move dexarmPicker towards laser box
    dexarmPicker.move_to(-395, 60, -35, 300, mode="G0", feedrate=speedRobot) #move dexarmPicker to point towards laser box
    dexarmPicker.move_to(-395, 60, -35, 100, mode="G0", feedrate=speedRobot) #move the dexarmPicker to the laser box
    dexarmPicker.move_to(-385, 50, -35, 40, mode="G0", feedrate=speedRobot) #move the coaster into the laser box
    dexarmPicker.air_picker_stop()
    dexarmPicker.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarmPicker back to move out of laser box
    dexarmPicker.move_to(-202, 0, 0, 700, mode="G0") #move dexarmPicker out of laser box
    dexarmPicker.move_to(-201, 0, 0, 700, mode="G1") #move dexarm out of laser box

def laserPickUp(dexarmPicker, dexarmLaser):
    #speedRobot = 6000
    dexarmLaser.move_to(-2, 300, 124, mode="G1", feedrate=speedRobot) #move laser dexarm up
    dexarmPicker.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm back into the laser box
    dexarmPicker.move_to(-385, 50, -60, 40, mode="G0", feedrate=speedRobot) #pick up the coaster inside the laser box
    dexarmPicker.air_picker_pick() #pick up the coaster
    dexarmPicker.move_to(-385, 50, -20, 40, mode="G0", feedrate=speedRobot) #move the dexarm up with the coaster
    dexarmPicker.move_to(-202, 0, 0, 60, mode="G0", feedrate=speedRobot) #move the dexarm back to move out of laser box
    dexarmPicker.move_to(-202, 0, 0, 300, mode="G0", feedrate=speedRobot) #move dexarm out of laser box

def get_filename(coasterVariant):
    file_map = { #Define an index of the GCODE files we need to use. For now, these are placeholders. 
        1: "outputGcode6.txt",
        # 1: "outputGcode5.txt",
        2: "outputGcode7.txt",
        3: "outputGcode8.txt",
        4: "outputGcode5.txt"
        # 4: "outputGcode8.txt"
    }
    if coasterVariant in file_map:
        return file_map[coasterVariant]
    else:
        raise RuntimeError(f"No filename available for coasterVariant index {coasterVariant}. Stopping execution. ")

def EngraveCoaster(dexarmPicker,dexarmLaser,coasterVariant): #Decalre coasterVariant as an int, from 1 to N
    import laser_module as l_m
    #speedRobot = 6000

    dexarmPicker.move_to(0,240,0,880,mode="G0",feedrate=speedRobot) #Make sure that the arm is out of the way. 
    time.sleep(5) # 5-second wait to allow arm to move
    l_m.LaserDoorOpen()  
    laserDropOff(dexarmPicker, dexarmLaser) #TODO: Modify this module to use relative coordinates for sanity reasons. 
    time.sleep(20) # 5-second wait to allow door to close
    l_m.LaserDoorClose()

    time.sleep(10) #10-second wait to allow the door to be manipulated. 

    #Use the filename mapping function defined previous to grab the correct filename from a list. 
    fileName = get_filename(coasterVariant)
    print("Currently attempting to engrave " + fileName) #I love Python's mixed expression syntax. Makes so much sense. 

    l_m.runLaser(dexarmLaser, fileName) 
    print("Laser would be running here, except Alex doesn't trust the box to close properly.")
    time.sleep(5)

    l_m.LaserDoorOpen()
    laserPickUp(dexarmPicker, dexarmLaser) #Grab the coaster from the laser box, then continue with your business. 

