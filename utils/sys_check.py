# Imports

import os
import sys
import subprocess

# Custom Imports

from utils.logger.logger import loggingF

def checkRoot():

    if os.geteuid() != 0:

        loggingF(4, "The script was tried to be run without being root")

        print("This script must be run as root. Please run with sudo or as root user.")
        
        sys.exit(1)

def getServiceStatus(service_name):
    try:
        result = subprocess.run(
            ['systemctl', 'list-unit-files', f'{service_name}.service'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        exists = service_name in result.stdout
        return exists
        
    except Exception as e:
        print(f"Error checking service: {e}")
        return False

def checkRoot():

    if os.geteuid() != 0:

        loggingF(4, "The script was tried to be run without being root")

        print("This script must be run as root. Please run with sudo or as root user.")
        
        sys.exit(1)

def getServiceStatus(service_name):
    try:
        result = subprocess.run(
            ['systemctl', 'list-unit-files', f'{service_name}.service'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        exists = service_name in result.stdout
        return exists
        
    except Exception as e:
        print(f"Error checking service: {e}")
        return False

def getFullStatus(service_name):
    try:
        # Ejecutamos 'systemctl status'
        output = subprocess.check_output(['systemctl', 'status', service_name], 
                                         universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def checkPermission(appPath):

    if os.access(appPath, os.X_OK):

        loggingF(2, "The script was found and is executable")
    else:

        loggingF(4, "The script was not found or is not executable")

        try:
                os.chmod(appPath, 0o755)

                loggingF(2, "Permissions have been updated to make the script executable")
        
        except Exception as e:
               
                loggingF(4, f"Failed to update permissions: {e}")
                
                print("Error with executing the app. Please check the details on the logs")




