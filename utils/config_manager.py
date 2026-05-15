# Imports


import os
import getpass
import subprocess
import configparser

# Custom Imports

from utils.observability import *
from utils.colors import Theme as T
from utils.sys_check import *

# Init configParser

config = configparser.ConfigParser()

# Paths to config.ini to solve bad imports

baseDir = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(baseDir, '..', '..', 'config.ini')

# Read config.ini

filesRead = config.read(configPath)

# Exception to not reading .ini

if not filesRead:
    loggingF(4, f"No se pudo encontrar o leer el archivo config en: {configPath}")
    exit(1)

# configGet function
# Objetive: Get values of the config.ini

def configGet(sectionC, optionC):

    loggingF(1, f"Searching in config for section {sectionC} with value {optionC}")
    
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

# inv function
# Objetive: Debug Function to check
# if the inventory is working correctly

def inv():

    print("--- Inventory Script ---")

    invPath = os.path.join("appInv", "getInv.py")

    checkPermission(invPath)

    result = subprocess.run(["ansible-inventory", "-i", invPath, "--list"], capture_output=True, text=True)
    
    if result.returncode != 0:
        
        loggingF(4, result.stderr)
        
        print("Error running inventory script. Check logs for details.")
    else:
        
        print(result.stdout)
