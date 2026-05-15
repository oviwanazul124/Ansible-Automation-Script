# Imports

import os
import subprocess
import sys

# Custom Imports

from utils.colors import Theme as T
from utils.logger.logger import loggingF
from utils.checkRoot.checkRoot import checkRoot

def deployService(status):

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(CURRENT_DIR)

    print(root_dir)

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

    stateFile = os.path.join(root_dir, "deployed_hosts.txt")
    
    if os.path.exists(stateFile):
        os.remove(stateFile)

    # Write Service 

    if status == False:
            try:

                print(f"{T.BOLD} [?] Trying to write the .service {T.RESET}")

                loggingF(1, f"Writing service file to {unit_file_path}")

                with open(unit_file_path, "w") as f:
                    f.write(service_config)

                print(f"{T.BOLD} {T.GREEN} [OK] .service was written correctly. {T.RESET}")

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

        print(f"{T.GREEN} {T.BOLD} [OK] Service {serviceName} enabled on boot {T.RESET}")

    except Exception as e:

        print(f"{T.GOLD} {T.BOLD} [X] There was an error enabling the {serviceName} on boot, please check the logs for more info. {T.RESET}")

        loggingF(4, f"Error enabling the service on boot: {e}")

        input("» ")    

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