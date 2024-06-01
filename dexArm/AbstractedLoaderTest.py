from PickerLoadingModule import grabCoaster, initialize_picker_arm
from PickerUnloadingModule import deposit_coaster
from PickVerificationModule import pickStatus
from pydexarm import Dexarm
import time

# Constants
N = 100  # Number of times to repeat the process
 
def main():
    # Initialize the Dexarm (in this case picker)
    dexarm = Dexarm(port='COM19')

    # If the picker arm needs to be initialized
    initialize_picker_arm(dexarm)  # Uncomment this line if initialization is required

    for _ in range(N):
        # Grab the coaster
        grabCoaster(dexarm)  
        
        # Optional delay (personal preference)
       # time.sleep(1)

        # Drop the coaster
        deposit_coaster(dexarm)

        # Additional delay to observe the process (optional)
        #time.sleep(1)

    # Properly close the connection to the Dexarm after operations
    #dexarm.close() #Keep dexarm open, actually. 

if __name__ == "__main__":
    main()


