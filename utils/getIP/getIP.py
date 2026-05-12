from utils.logger.logger import loggingF
import subprocess
import os
import utils.checkPermission.chkPerm as checkPermission

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