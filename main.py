# Imports

import subprocess
import os

def clear():
    subprocess.run(["clear"])

def inv():
    print("--- Inventory Script ---")
    invPath = os.path.join("appInv", "getInv.py")
    result = subprocess.run(["ansible", "-i", invPath, "--list"], capture_output=True, text=True)
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