# Imports

import os
import getpass
import subprocess
import configparser

# Custom Imports

from utils.observability import loggingF
from utils.colors import Theme as T
from utils.sys_check import checkPermission
from paths import config_path, vault_file_path, vault_pass_file_path, inv_path

# configGet function
# Objetive: Get values of the config.ini

config = configparser.ConfigParser()

filesRead = config.read(config_path)

def configGet(sectionC, optionC):

    # Init configParser

    loggingF(1, f"Searching in config for section {sectionC} with value {optionC}")
    
    print(config_path)

    try:
        
        return config.get(sectionC, optionC)
    
    except configparser.NoSectionError:
        
        loggingF(4, f"The section [{sectionC}] dosen't exists in config.ini")
        
        raise
    
    except configparser.NoOptionError:
        
        loggingF(4, f"The option '{optionC}' dosen't exists for this [{sectionC}]")
        
        raise

# vaultConfig function
# Objetive: This function is responsible for creating
# the vault to store the SUDO password for the remote hosts
# and the SSH one.

def vaultConfig():

    # Check if vault password file exists, if not create it and set permissiosn to 600

    if not os.path.exists(vault_pass_file_path):

        aPass = getpass.getpass(f"{T.BOLD} Enter master password for Ansible Vault » {T.RESET}")

        try:
            with open(vault_pass_file_path, 'w') as f:

                f.write(aPass)

            os.chmod(vault_pass_file_path, 0o600)

        except Exception as e:
            loggingF(4, f"Error creating vault password file: {e}")


        loggingF(1, f"Created vault password file: {vault_pass_file_path}")

        print(f"{T.GREEN} {T.BOLD} [OK] Master Password stored {T.RESET}")

    # Check if vault file exists, if not create it with the SUDO password for the remote hosts and the SSH one.

    if not os.path.exists(vault_file_path):

        loggingF(1,f"Creating new encrypted vault file: {vault_file_path}")

        depPass = getpass.getpass(f"{T.BOLD} Enter the SUDO password for remote hosts » {T.RESET}")

        content = f"ansible_become_password: {depPass}\ninitial_device_password: {depPass}"

        print(f"{T.GREEN} {T.BOLD} [OK] Sudo Password stored {T.RESET}")

        cmd = [
            "ansible-vault", "encrypt",
            "--vault-password-file", vault_pass_file_path,
            "--output", vault_file_path,
            "-"
        ]

        # Try to encode the contents of the Ansible Vault

        try:
    
            subprocess.run(
                cmd,
                input=content.encode(),
                capture_output=True,
                check=True
            )

            print(f"{T.GREEN} {T.BOLD} [OK] Vault file encrypted successfully. {T.RESET}")

        # If fails remove it to not save corrupted files

        except subprocess.CalledProcessError as e:

            print(f"Error creating vault: {e.stderr.decode()}")

            if os.path.exists(vault_file_path):

                os.remove(vault_file_path)

# inv function
# Objetive: Debug Function to check
# if the inventory is working correctly

def inv():

    print("--- Inventory Script ---")

    checkPermission(inv_path)

    result = subprocess.run(["ansible-inventory", "-i", inv_path, "--list"], capture_output=True, text=True)
    
    if result.returncode != 0:
        
        loggingF(4, result.stderr)
        
        print("Error running inventory script. Check logs for details.")
    else:
        
        print(result.stdout)
