# Imports

import subprocess
import sys
import os
import yaml

# Custom Imports

from utils.colors import Theme as T
from utils.sys_check import loggingF, checkPermission, getServiceStatus
from utils.observability import erHandler
from utils.config_manager import configGet
from paths import *

# sshDeploy function
# Objetive: Deploy the SSH key to the hosts in the inventory file or
# the one not detect if it is running in automatic mode.

# Get configs

remote_user = configGet('users', 'remote_user')

def sshDeploy():

    # Detect if public key is created or in config.ini

    if not os.path.exists(os.path.expanduser("~/.ssh/id_rsa.pub")):

        loggingF(3, "SSH public key not found. Generating SSH public key")
        
        try:
            subprocess.run(["ssh-keygen", "-t", "rsa", "-N", "", "-f", os.path.expanduser("~/.ssh/id_rsa")], check=True)

            loggingF(1, "SSH public key generated successfully")

        except subprocess.CalledProcessError as e:

            loggingF(4, f"Error generating SSH public key: {e}")

    # Create enveiorement for host check

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    checkPermission(inv_path)

    # Ansible playbook to deploy SSH key

    command = [
        "ansible-playbook",
        "-i", inv_path,
        sshPlaybook_path,
        "-u", remote_user,
        "-k",
        "--ssh-common-args=-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    ]

    try:

        subprocess.run(command, check=True, env=env)

        loggingF(1, "SSH key deployed succesfully")

        print("SSH key deployed successfully. For all the available host, for checking the host use the inventory option")

    except subprocess.CalledProcessError as e:

        loggingF(4, f"Error running sshDeploy: {e}")

# generatePkgPlaybook function
# Objetive: Generate or regenerate the playbook destinated to be used
# by the system daemon

def generatePkgPlaybook():


    # Check if the playbook directoy exists
    # if not create it

    if not os.path.exists(playbook_dir):

        os.makedirs(playbook_dir)

    # Check if the playbook was created before if it is the case remove it

    if os.path.exists(playbook_path):

        os.remove(playbook_path)

    print(f"{T.BOLD} \n--- Configuración de Paquetes --- {T.RESET}")

    print("Enter the packages you want to create, separated by commas:")

    print("Example: vim, htop, curl, git")
    
    user_input = input(f"{T.BOLD} [?] Paquetes » {T.RESET}")

    pkg_list = [p.strip() for p in user_input.split(",") if p.strip()]

    # If it is not included any package create a blank file

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

    # Put the info in it

    try:

        with open(playbook_path, "w") as f:

            yaml.dump(playbook_data, f, default_flow_style=False, sort_keys=False)
            f.flush()        
            os.fsync(f.fileno())


        loggingF(1, f"Playbook Saved in: {playbook_path}")

    except Exception as e:

        erHandler(e)

        print(f"{T.GOLD} {T.BOLD} [X] There was an error creating the files, please check the logs for more information. {T.RESET}")

    existService = getServiceStatus(serviceName)

    deployService(existService)

# aptDeploy function
# Objetive: This function is responsible for deploying the applications using Ansible playbooks.
# It take a package or a list of packages as an argument and runs the ansible playbook to install the packages on the targets machines.

def aptDeploy():

    packg = input(f"{T.BOLD} Enter the packages to install as example nginx, git » {T.RESET}")

    # Create envenvironment variable to disable key checking on Ansible

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    # Get all the paths and variables need to run the script correctly

    # Inv file path and permissions check
    
    checkPermission(inv_path)

    # Correct formating of the input, if the input is a list of packages, we will
    # convert it from git htop to "htop, git", if it is a single package, we will
    # keep it as it is

    if isinstance(packg, list):
        packages_val = ",".join(packg)
    else:
        packages_val = packg

    # Command Line to run the ansible playbook

    command = [
        "ansible-playbook",
        "-i", inv_path,
        aptPlaybook_path,
        "-u", remote_user,
        "-e", f"my_packages={packages_val}",
        "-k",
        "-K",
        "--ssh-common-args=-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    ]

    try:

        subprocess.run(command, check=True, env=env)

        loggingF(1, "Apps installed correctly")

        print(f"{T.GREEN} {T.BOLD} [OK] All the apps that was mentioned on the playbook was installed succesfully {T.RESET}")

    except subprocess.CalledProcessError as e:

        loggingF(4, f"Error running AppDeploy: {e}")

        print(f"{T.GOLD} {T.BOLD} [X] There was an error deploying the apps, please checks the logs for more info {T.RESET}")

# install_dependencies function
# Objetive: Install dependencies of the script

def install_dependencies():

    for package in dependencies:
        
        try:

            __import__(package)

        except ImportError:

            loggingF(2, f"{package} not found. Attempting to install")
           
            try:
                
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                
                loggingF(2, f"{package} installed succesfully")
            
            except Exception as e:
                
                loggingF(4, f"Failed to install {package}: {e}")
                
                sys.exit(1)


def deployService(status):

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

ExecStart={sys.executable} -u {script_path}

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

    if os.path.exists(stateFile_path):
        os.remove(stateFile_path)

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