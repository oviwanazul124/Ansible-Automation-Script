import subprocess
import sys
from utils.logger.logger import loggingF

def install_dependencies():

    dependencies = ["scapy"]

    for package in dependencies:
        try:

            __import__(package)
        except ImportError:
            loggingF(2, f"{package} not found. Attempting to install")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                loggingF(2, f"{package} installed succesfully")
            except Exception as e:
                loggingF(4, f"Failed to install {package}: {e}")
                sys.exit(1)