#!/usr/bin/env python3

# Imports

import os
import getpass
import subprocess

# Custom Imports

from utils.colors import Theme as T
from utils.logger.logger import loggingF
from utils.errorsHandler.errorHandler import erHandler

# vaultConfig function
# Objetive: This function is responsible for creating
# the vault to store the SUDO password for the remote hosts
# and the SSH one.

def vaultConfig():

    # Path working to not get import errors and make easier use.

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(CURRENT_DIR)

    vaultFile = os.path.join(root_dir, 'pass.yml')

    vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')

    # Check if vault password file exists, if not create it and set permissiosn to 600

    if not os.path.exists(vaultPassFile):

        aPass = getpass.getpass(f"{T.BOLD} Enter master password for Ansible Vault » {T.RESET}")

        try:
            with open(vaultPassFile, 'w') as f:

                f.write(aPass)

            os.chmod(vaultPassFile, 0o600)

        except Exception as e:
            loggingF(4, f"Error creating vault password file: {e}")


        loggingF(1, f"Created vault password file: {vaultPassFile}")

        print(f"{T.GREEN} {T.BOLD} [OK] Master Password stored {T.RESET}")

    # Check if vault file exists, if not create it with the SUDO password for the remote hosts and the SSH one.

    if not os.path.exists(vaultFile):

        loggingF(1,f"Creating new encrypted vault file: {vaultFile}")

        depPass = getpass.getpass(f"{T.BOLD} Enter the SUDO password for remote hosts » {T.RESET}")

        content = f"ansible_become_password: {depPass}\ninitial_device_password: {depPass}"

        print(f"{T.GREEN} {T.BOLD} [OK] Sudo Password stored {T.RESET}")

        cmd = [
            "ansible-vault", "encrypt",
            "--vault-password-file", vaultPassFile,
            "--output", vaultFile,
            "-"
        ]

        try:

            result = subprocess.run(
                cmd,
                input=content.encode(),
                capture_output=True,
                check=True
            )

            print(f"{T.GREEN} {T.BOLD} [OK] Vault file encrypted successfully. {T.RESET}")

        except subprocess.CalledProcessError as e:

            print(f"Error creating vault: {e.stderr.decode()}")

            if os.path.exists(vaultFile):

                os.remove(vaultFile)
