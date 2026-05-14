#!/usr/bin/env python3

# Imports

import os
import subprocess
import sys

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger.logger import loggingF
from utils.configR.configR import configGet
from utils.checkPermission.chkPerm import checkPermission

# sshDeploy function
# Objetive: Deploy the SSH key to the hosts in the inventory file or
# the one not detect if it is running in automatic mode.

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

    # Getting paths for all of them

    inv = os.path.join("appInv", "getInv.py")

    checkPermission(inv)

    sshPlaybook = os.path.join("playbooks", "SSHDeploy.yml")

    remote_user = configGet('users', 'remote_user')

    # Ansible playbook to deploy SSH key

    command = [
        "ansible-playbook",
        "-i", inv,
        sshPlaybook,
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
        