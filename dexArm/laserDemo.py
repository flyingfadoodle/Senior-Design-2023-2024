#Add Laser Module:
import sys
sys.path.insert(0, 'LaserModule')
import laser_module as l_m

#Import Movement Module:
sys.path.insert(0, 'MovementModule')
from pydexarm import Dexarm


if __name__ == "__main__":
    #Establish connection with Laser Arm:  
    laserDexarm = Dexarm(port="COM6");

    #Initialize Arm:
    laserDexarm.go_home();
    
    #Run Laser
    l_m.runLaser(laserDexarm)