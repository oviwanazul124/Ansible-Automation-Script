
# Imports

import sys
import os
import yaml

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.colors import Theme as T
from utils.logger.logger import loggingF
from utils.errorsHandler.errorHandler import erHandler
from utils.checkService.checkService import getServiceStatus
from utils.deployService.deployService import deployService

def generatePkgPlaybook(root_dir):

    playbook_dir = os.path.join(root_dir, "playbooks")

    playbook_path = os.path.join(playbook_dir, "InstallPackages.yml")

    if not os.path.exists(playbook_dir):

        os.makedirs(playbook_dir)

    if os.path.exists(playbook_path):

        os.remove(playbook_path)

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

        # Justo después de yaml.dump...
        if os.path.exists(playbook_path):
            print(f"{T.GREEN} [DEBUG] Confirmado: El archivo existe físicamente. {T.RESET}")
            print(f" [DEBUG] Tamaño del archivo: {os.path.getsize(playbook_path)} bytes")
        else:
            print(f"{T.RED} [DEBUG] ERROR: Python dice que lo guardó, pero el archivo NO existe. {T.RESET}")

            print(f"{T.GREEN} {T.BOLD} [OK] Playbook with the following packages {len(pkg_list)} has been saved. {T.RESET}")
            
    except Exception as e:

        erHandler(e)

        print(f"{T.GOLD} {T.BOLD} [X] There was an error creating the files, please check the logs for more information. {T.RESET}")

    serviceName = 'watchdog-Ansible'

    existService = getServiceStatus(serviceName)

    deployService(existService)

