# Imports

import os
import subprocess
import sys

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger.logger import loggingF
from utils.configR.configR import configGet
from utils.checkPermission.chkPerm import checkPermission

def aptDeploy():

    # Create enveiorement for host check

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    # Getting all the variables and paths

    inv = os.path.join("appInv", "getInv.py")
    checkPermission(inv)
    aptPlaybook = os.path.join("playbooks", "AppInstall.yml")
    remote_user = configGet('users', 'remote_user')

    # Ansible playbook to install the apps

    command = [
        "ansible-playbook",
        "-i", inv,
        aptPlaybook,
        "-u", remote_user,
        "-k",
        "-K",
        "--ssh-common-args=-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    ]

    try:

        subprocess.run(command, check=True, env=env)
        loggingF(1, "Apps installed correctly")
        print("All the apps that was mentioned on the playbook was installed succesfully")

    except subprocess.CalledProcessError as e:
        loggingF(4, f"Error running AppDeploy: {e}")
