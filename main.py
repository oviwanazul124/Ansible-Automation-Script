# Imports

import subprocess
import os

# Custom Imports

from utils.logger.logger import loggingF
from utils.checkPermission.chkPerm import checkPermission
from ansible_menus import *

def clear():
    subprocess.run(["clear" if os.name == "posix" else "cls"], shell=True)

def menuWrapper(title, menuDict):
    while True:
        clear()
        print(f'--- {title} ---')
        for key, value in menuDict.items():
            print(f'{key}. {value['label']}')
        
        opt = input("\nSelect an option: ")

        if opt in menuDict:
            item = menuDict[opt]

            if item['label'] in ['Exit', 'Back to Main'] or item['func'] is None:
                break

            if item['func'] == 'debugMenu':
                menuWrapper("Debug Menu", debugMenu)
            elif item['func'] == 'confMenu':
                menuWrapper("Configuration Menu", confMenu)
            else:
                item['func']()
                input("\nPress Enter to continue...")
        else:
            print("Invalid option.Please try again.")
            input()


#def debug_menu():
#    while True:
#        clear()
#        print("--- Debug Menu ---")
#        print("1. Check devices actives in the network")
#        print("2. Exit")

    

#def main_menu():
#    while True:
#        clear()
#        print("--- Ansible Menu ---")
#        print("1. Run Inventory Script")
#        print("2. Deploy SSH key")
#        print("3. Install Required Packages")
#        print("4. Exit")
#
#        opt = input("\n Select an option:")
#
#        if opt == "1":
#            inv()
#            input("\nPress Enter to continue...")
#        elif opt == "2":
#            sshDeploy()
#            input("\nPress Enter to continue...")
#        elif opt == "3":
#            package = input("Enter the packages to install as example nginx, git: ")
#            aptDeploy(package)
#            input("\nPress Enter to continue...")
#        elif opt == "4":
#            break

if __name__ == "__main__":
    menuWrapper("Ansible Menu", menuMain)