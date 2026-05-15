# Imports

import os

# Custom Imports

from appWatchDogDeploy.WatchdogDeploy import deployWatchdog
from utils.colors import Theme as T
from utils.deployment_engine import sshDeploy, install_dependencies, generatePkgPlaybook, aptDeploy
from utils.sys_check import Checklog, getFullStatus
from utils.config_manager import inv, vaultConfig
from utils.observability import projectRoot

logs_dir = projectRoot() / "logs" / "log.log"

menuMain = {
    "1": {
        "label": "[?] Enter Debug Menu",
        "func": "debugMenu"
    },
    "2": {
        "label": "[~] Enter Configuration Menu",
        "func": "confMenu"
    },
    "3": {
        "label": "[^]  Enter Deployment Menu",
        "func": "deployMenu"
    },
    "4": {
        "label": "[Q] Exit",
        "func": lambda: None
    }
}

debugMenu = {
    "1": {
        "label": "[?] Check devices actives in the network",
        "func": inv
    },

    "2": {
        "label": "[^] Deploy SSH Key",
        "func": sshDeploy
    },

    "3": {
        "label": "[^] Install Dependencies",
        "func": lambda: install_dependencies
    },

    "4": {
        "label": "[?] Check logs",
        "func": lambda: Checklog(logs_dir)
    },

    "5": {
        "label": "[?] Check Status of service",
        "func": lambda: getFullStatus("watchdog-Ansible")
    },

    "6": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}


confMenu = {
    "1": {
        "label": "[?] Configure Ansible Vault",
        "func": lambda: vaultConfig
    },

    "2": {
        "label": "[?] Modify Service Playbook",
        "func": lambda: generatePkgPlaybook(root_dir)
    },

    "3": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}

deployMenu = {
    "1": {
        "label": "[^] Inmediate Deployment",
        "func": lambda: aptDeploy(input(f"{T.BOLD} Enter the packages to install as example nginx, git » {T.RESET}"))
    },

    "2": {
        "label": "[^] Automatic Deployment",
        "func": lambda: deployWatchdog
    },

    "3": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}