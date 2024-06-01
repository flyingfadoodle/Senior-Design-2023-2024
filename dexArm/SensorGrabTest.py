import time
from TOFSensorModule import get_sensor_height, close_sensor
from pydexarm import Dexarm

# Configurable coordinates and settings
loading_X = 316
loading_Y = 54
loading_hover_Z = 80
#Z_correction = -5  # removed this variable; will instead lump into calibrated height (see TOFSensorModule)
speedRobot = 6000
slow_feedrate = 1000  # Slower feedrate for the final approach
loading_clearance_X = 50; 


def main():
    # Initialize the Dexarm
    dexarm = Dexarm(port='COM19')

    try:
        # Home the arm
        dexarm.go_home()

        # Move to a clearance position before going directly above the coaster
        dexarm.move_to(loading_X - 100, loading_Y, loading_hover_Z, mode="G0", feedrate=speedRobot)

        # Move to the hover position above the coaster stack
        dexarm.move_to(loading_X, loading_Y, loading_hover_Z, mode="G1", feedrate=speedRobot)

        # Take a sensor reading
        height = get_sensor_height()
        print(f"Sensor height measurement: {height} mm")
        
        # Uncomment the following lines for full operation after initial tests
        
        # Use the sensor reading to adjust the picker height
        if height is not None:
            # Move quickly to 10 mm above the target Z
            target_Z_quick = loading_hover_Z - height  + 10
            dexarm.move_to(loading_X, loading_Y, target_Z_quick, mode="G1", feedrate=speedRobot)

            # Move slowly for the last 10 mm
            target_Z_slow = loading_hover_Z - height
            dexarm.move_to(loading_X, loading_Y, target_Z_slow, mode="G1", feedrate=slow_feedrate)

            # Initialize the vacuum picker
            dexarm.air_picker_pick()

            # Move the arm backwards in X, and back up to its hover height
            dexarm.move_to(loading_X - loading_clearance_X, loading_Y, loading_hover_Z, mode="G1", feedrate=speedRobot)

            time.sleep(5) #Wait 5 seconds 

            dexarm.air_picker_stop() #...then drop the coaster
        

    finally:
        # Ensure to close connections properly
        close_sensor()
        dexarm.close()

if __name__ == "__main__":
    main()


