# Imports

import sys
import os
import subprocess

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger.logger import loggingF
from utils.checkRoot.checkRoot import checkRoot
from utils.checkPermission.chkPerm import checkPermission
from utils.errorsHandler.errorHandler import erHandler
from appVaultConfig.vaultConfig import vaultConfig

def deployWatchdog():

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(CURRENT_DIR)

    vaultFile = os.path.join(root_dir, 'pass.yml')

    vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')

    invPath = os.path.join(root_dir, "appInv", "getInv.py")


    existService = False

    try:

        subprocess.run(
            ["systemctl", 'list-unit-files', 'watchdog-Ansible.service'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        existService = True
    
    except Exception as e:

        loggingF(1, 'There was an error checking for the watchdog service: ' + str(e) )
    
    if existService == False:
    
        print("This will add the watchdog service to the machine. Are you sure? (y/n)")

        answer = input().lower()

        if answer == 'y':
            
            if not os.path.exists(vaultFile) or not os.path.exists(vaultPassFile):
                
                loggingF(1, "Vault files wasn't found, calling appVaultConfig to create them.")
            
                print("There isn't a Ansible Vault configuration on this machine please configure it now")
                
                input("Press enter to continue...")
                
                vaultConfig()

            print("Checking all files and permissions...")

            try:

                checkPermission(invPath)

            except Exception as e:

                loggingF(1, 'There was an error checking permissions: ' + str(e))

                print("Error checking permissions, please check the logs for more information")

                input("Press enter to end the program...")

                sys.exit(1)

            try:

                checkRoot()

            except Exception as e:

                loggingF(1, "There was an error checking for root permissions:" + str(e))

                print("There was an error checking for root permissions, please check the logs for more information")

                input("Press enter to end the program...")

                sys.exit(1)
        
        


        else:
            pass