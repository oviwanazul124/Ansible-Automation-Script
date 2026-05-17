# Imports

import sys
import os

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.colors import Theme as T
from utils.observability import loggingF
from utils.sys_check import getServiceStatus, checkPermission, checkRoot
from utils.config_manager import vaultConfig
from utils.deployment_engine import generatePkgPlaybook
from paths import vault_file_path, serviceName, vault_pass_file_path, inv_path

def deployWatchdog():

    existService = getServiceStatus(serviceName)

    if existService == False:
    
        print(f"{T.GOLD} {T.BOLD} [!] This will add the watchdog service to the machine. Are you sure? (y/n) {T.RESET}")

        answer = input("» ").lower()

        if answer == 'y':
            
            if not os.path.exists(vault_file_path) or not os.path.exists(vault_pass_file_path):
                
                loggingF(1, "Vault files wasn't found, calling appVaultConfig to create them.")
            
                print(f"{T.GOLD} {T.BOLD} [!] There isn't a Ansible Vault configuration on this machine please configure it now {T.RESET}")
                
                input(f"{T.BOLD} Press enter to continue » {T.RESET}")
                
                vaultConfig()

                print(f"{T.GREEN} {T.BOLD} [OK] Ansible Vault Correctly configured {T.RESET}")

            print(f"{T.BOLD} [?] Checking all files and permissions {T.RESET}")

            try:

                checkPermission(inv_path)

                print(f"{T.GREEN} {T.BOLD} [OK] Permission checked and working correctly. {T.RESET}")

            except Exception as e:

                loggingF(1, 'There was an error checking permissions: ' + str(e))

                print(f"{T.GOLD} {T.BOLD} [X] Error checking permissions, please check the logs for more information {T.RESET}")

                input(f"{T.BOLD} Press enter to end the program » {T.RESET}")

                sys.exit(1)

            try:

                checkRoot()

                print(f"{T.GREEN} {T.BOLD} [OK] Script Running as root checked. {T.RESET}")

            except Exception as e:

                loggingF(1, "There was an error checking for root permissions:" + str(e))

                print(f"{T.GOLD} {T.BOLD} [X] There was an error checking for root permissions, please check the logs for more information {T.RESET}")

                input(f"{T.BOLD} Press enter to end the program » {T.RESET}")

                sys.exit(1)

            generatePkgPlaybook()

    else:

        print(f"{T.GOLD} {T.BOLD} [X] The service is already running {T.RESET}")

        pass
    