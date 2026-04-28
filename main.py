# Imports

import subprocess
import os

# Custom Imports

from utils.logger.logger import loggingF
from utils.checkPermission.chkPerm import checkPermission


def clear():
    subprocess.run(["clear"])

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