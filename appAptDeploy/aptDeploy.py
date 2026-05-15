# Imports

import os
import subprocess
import sys

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.colors import Theme as T
from utils.logger.logger import loggingF
from utils.configR.configR import configGet
from utils.checkPermission.chkPerm import checkPermission

# aptDeploy function
# Objetive: This function is responsible for deploying the applications using Ansible playbooks.
# It take a package or a list of packages as an argument and runs the ansible playbook to install the packages on the targets machines.

def aptDeploy(packg):

    # Create envenvironment variable to disable key checking on Ansible

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    # Get all the paths and variables need to run the script correctly

        # Inv file path and permissions check

    inv = os.path.join("appInv", "getInv.py")
    checkPermission(inv)

        # aptPlayBook path

    aptPlaybook = os.path.join("playbooks", "AppInstall.yml")
    
        # Remote user path
    remote_user = configGet('users', 'remote_user')
    
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
        "-i", inv,
        aptPlaybook,
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
