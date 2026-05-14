# Imports

import os
import sys

# Custom Imports

from utils.logger.logger import loggingF

# Main function

def checkRoot():

    if os.geteuid() != 0:

        loggingF(4, "The script was tried to be run without being root")

        print("This script must be run as root. Please run with sudo or as root user.")
        
        sys.exit(1)