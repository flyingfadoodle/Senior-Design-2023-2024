"""
In the future, this module will have more robust error handling capabilities. For now, it just shuts off the air picker so it doesn't annoy anyone if the code crashes. 

(This code doesn't even stop exectuion, it just runs code before a RuntimeException is thrown elsewhere.)"""

from pydexarm import Dexarm

def stopWorkcell(dexarm):
   """Stops the workcell, currently in the event of the error. Taxes in the Picker arm object, for the purposes of stopping the air picker. 
   
   TODO: Make it so that this also stops the laser module, for safety reasons."""

   dexarm.air_picker_stop()

   #For some reason, running this exact line of code inline with the other Modules won't work. So it gets its own module1
   #That's it. That's literally all this function does. - Alex

