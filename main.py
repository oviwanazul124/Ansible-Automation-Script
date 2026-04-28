# Imports

import subprocess
import os
from utils.logger.logger import loggingF

def clear():
    subprocess.run(["clear"])

def inv():
    print("--- Inventory Script ---")
    invPath = os.path.join("appInv", "getInv.py")

    if os.access(invPath, os.X_OK):
        loggingF(2, "The script was found and is executable")
    else:
        loggingF(4, "The script was not found or is not executable")

        try:
                os.chmod(invPath, 0o755)
                loggingF(2, "Permissions have been updated to make the script executable")
        except Exception as e:
                loggingF(4, f"Failed to update permissions: {e}")
                print("Error with executing the app. Please check the details on the logs")

    result = subprocess.run(["ansible-inventory", "-i", invPath, "--list"], capture_output=True, text=True)
    if result.returncode != 0:
        loggingF(4, result.stderr)
        print("Error running inventory script. Check logs for details.")
    else:
        print(result.stdout)

def menu():
    while True:
        clear()
        print("--- Ansible Menu ---")
        print("1. Run Inventory Script")
        print("2. Exit")

        opt = input("\n Select an option:")

        if opt == "1":
            inv()
            input("\nPress Enter to continue...")
        elif opt == "2":
            break

if __name__ == "__main__":
    menu()