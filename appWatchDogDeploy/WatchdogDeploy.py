# Imports

import sys
import os
import subprocess
import yaml

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.colors import Theme as T
from utils.logger.logger import loggingF
from utils.checkRoot.checkRoot import checkRoot
from utils.checkPermission.chkPerm import checkPermission
from utils.errorsHandler.errorHandler import erHandler
from appVaultConfig.vaultConfig import vaultConfig

def generatePkgPlaybook(root_dir):

    playbook_dir = os.path.join(root_dir, "playbooks")

    playbook_path = os.path.join(playbook_dir, "InstallPackages.yml")

    if not os.path.exists(playbook_dir):

        os.makedirs(playbook_dir)

    print(f"{T.BOLD} \n--- Configuración de Paquetes --- {T.RESET}")

    print("Enter the packages you want to create, separated by commas:")

    print("Example: vim, htop, curl, git")
    
    user_input = input(f"{T.BOLD} [?] Paquetes » {T.RESET}")

    pkg_list = [p.strip() for p in user_input.split(",") if p.strip()]

    if not pkg_list:

        loggingF(2, "There wasn't any packages specified creating a blank file.")

        print(f"{T.GOLD} {T.BOLD} [!] There wasn't any package introduced, creating a blank file {T.RESET}")
        return

    playbook_data = [{
        "name": "Instalacion Automatica de Paquetes mediante Watchdog",
        "hosts": "all",
        "become": True,
        "tasks": [
            {
                "name": "Asegurar que los paquetes estan instalados",
                "ansible.builtin.package": {
                    "name": pkg_list,
                    "state": "present"
                }
            }
        ]
    }]

    try:

        with open(playbook_path, "w") as f:

            yaml.dump(playbook_data, f, default_flow_style=False, sort_keys=False)

        loggingF(1, f"Playbook Saved in: {playbook_path}")

        print(f"{T.GREEN} {T.BOLD} [OK] Playbook with the following packages {len(pkg_list)} has been saved. {T.RESET}")

    except Exception as e:

        erHandler(e)

        print(f"{T.GOLD} {T.BOLD} [X] There was an error creating the files, please check the logs for more information. {T.RESET}")

def deployWatchdog():

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(CURRENT_DIR)

    vaultFile = os.path.join(root_dir, 'pass.yml')

    vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')

    invPath = os.path.join(root_dir, "appInv", "getInv.py")

    serviceName = 'watchdog-Ansible'

    scriptPath = os.path.join(root_dir, "appWatchDog", "watchdog.py")

    unit_file_path = f"/etc/systemd/system/{serviceName}.service"

    service_config = f"""[Unit]
Description=Ansible Network Monitor Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory={root_dir}

Environment=PYTHONPATH={root_dir}
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONUNBUFFERED=1

ExecStart={sys.executable} -u {scriptPath}

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

    existService = False

    if existService == False:
    
        print(f"{T.GOLD} {T.BOLD} [!] This will add the watchdog service to the machine. Are you sure? (y/n) {T.RESET}")

        answer = input("» ").lower()

        if answer == 'y':
            
            if not os.path.exists(vaultFile) or not os.path.exists(vaultPassFile):
                
                loggingF(1, "Vault files wasn't found, calling appVaultConfig to create them.")
            
                print(f"{T.GOLD} {T.BOLD} [!] There isn't a Ansible Vault configuration on this machine please configure it now {T.RESET}")
                
                input(f"{T.BOLD} Press enter to continue » {T.RESET}")
                
                vaultConfig()

                print(f"{T.GREEN} {T.BOLD} [OK] Ansible Vault Correctly configured {T.RESET}")

            print(f"{T.BOLD} [?] Checking all files and permissions {T.RESET}")

            try:

                checkPermission(invPath)

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

            generatePkgPlaybook(root_dir)

            # Write Service 

            try:

                print(f"{T.BOLD} [?] Trying to write the .service {T.RESET}")

                loggingF(1, f"Writing service file to {unit_file_path}")

                with open(unit_file_path, "w") as f:
                    f.write(service_config)

                print(f"{T.BOLD} {T.GREEN} [OK] .service was written correctly.")

            except Exception as e:

                print(f"{T.GOLD} {T.BOLD} [X] There was an error writing the .service, please check the logs for more info. {T.RESET}")

                loggingF(4, f"Error writing the .service: {e}")

                input("» ")

            # Reload Daemon

            try:

                loggingF(1, "Reloading system daemon...")

                print(f"{T.BOLD} [?] Trying to reload the daemon {T.RESET}")

                subprocess.run(["systemctl", "daemon-reload"], check=True)

                print(f"{T.GREEN} {T.BOLD} [OK] Daemon reloaded successfully. {T.RESET}")

            except Exception as e:

                print(f"{T.GOLD} {T.BOLD} [X] There was an error reloading the daemon, please check the logs for more info. {T.RESET}")

                loggingF(4, f"Error reloading the daemon: {e}")

                input("» ")                


            # Enable Service on boot

            try:

                loggingF(1, f"Enabling {serviceName} to start on boot...")

                print(f"{T.BOLD} [?] Enabling {serviceName} to start on boot {T.RESET}")
                
                subprocess.run(["systemctl", "enable", serviceName], check=True)

                print(f"{T.GREEN} {T.BOLD} [OK] Service {serviceName} enabled on boot")

            except Exception as e:

                print(f"{T.GOLD} {T.BOLD} [X] There was an error enabling the {serviceName} on boot, please check the logs for more info. {T.RESET}")

                loggingF(4, f"Error enabling the service on boot: {e}")

                input("» ")    

                pass

            # Starting the service

            try:

                loggingF(1, f"Trying to start the service {serviceName}")

                print(f"{T.BOLD} [?] Trying to start the service {T.RESET}")

                subprocess.run(["systemctl", "restart", serviceName], check=True)

                print(f"{T.GREEN} {T.BOLD} [OK] Service enabled correctly {T.RESET}")

            except Exception as e:
                
                print(f"{T.GOLD} {T.BOLD} [X] There was an error enabling the {serviceName}, please check the logs for more info. {T.RESET}")

                loggingF(4, f"Error enabling the service: {e}")

                input("» ")    

                pass

        else:
            pass