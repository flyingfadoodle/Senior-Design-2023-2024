from FuzzyFeetPlacementModule import Dexarm, pick_fuzzy_foot
import time

#This code is untested. To be tested later. 

def test_all_positions(dexarm):
    # Iterate over all positions in a 5x5 grid
    for y in range(1, 6):  # Columns 1 through 5
        for x in range(1, 6):  # Rows 1 through 5
            # Pick the fuzzy foot at the current index
            print(f"Picking fuzzy foot at index [{x},{y}]")
            pick_fuzzy_foot(dexarm, x, y)
            
            # Hold at home position for 5 seconds
            print("Returning to home position and holding for 5 seconds...")
            dexarm.go_home()
            time.sleep(5)  # Wait for 5 seconds at home position
            dexarm.go_home() #Home again to fix minor inaccuracies

def main():
    # Initialize the Dexarm
    dexarm = Dexarm(port="COM4")
    dexarm.go_home()  # Ensure starting from the home position

    # Test all positions
    test_all_positions(dexarm)

    print("Completed testing all positions.")

if __name__ == "__main__":
    main()

