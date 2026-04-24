# Checks Imports

import os
import sys

# Main function

def checkRoot():

    if os.geteuid() != 0:
        print("This script must be run as root. Please run with sudo or as root user.")
        sys.exit(1)
