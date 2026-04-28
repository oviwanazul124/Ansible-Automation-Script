# Imports

import os

# Custom Imports

from utils.logger.logger import loggingF


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





