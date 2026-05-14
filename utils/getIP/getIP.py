# Imports

import subprocess
import os

# Custom Imports

from utils.checkPermission.chkPerm import checkPermission
from utils.logger.logger import loggingF

# inv function
# Objetive: Debug Function to check
# if the inventory is working correctly

def inv():

    print("--- Inventory Script ---")

    invPath = os.path.join("appInv", "getInv.py")

    checkPermission(invPath)

    result = subprocess.run(["ansible-inventory", "-i", invPath, "--list"], capture_output=True, text=True)
    
    if result.returncode != 0:
        
        loggingF(4, result.stderr)
        
        print("Error running inventory script. Check logs for details.")
    else:
        
        print(result.stdout)
