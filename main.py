# Imports

import subprocess
import os

# Custom Imports

from utils.logger.logger import loggingF
from utils.checkPermission.chkPerm import checkPermission
from ansible_menus import *
from utils.menuWrapper.Wrapper import menuWrapper

if __name__ == "__main__":
    menuWrapper("Ansible Menu", menuMain)