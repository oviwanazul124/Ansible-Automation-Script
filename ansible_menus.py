# Custom Imports

from appWatchDogDeploy.WatchdogDeploy import deployWatchdog
from utils.deployment_engine import sshDeploy, install_dependencies, generatePkgPlaybook, aptDeploy
from utils.sys_check import Checklog, getFullStatus
from utils.config_manager import inv, vaultConfig

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
        "func": install_dependencies
    },

    "4": {
        "label": "[?] Check logs",
        "func": Checklog
    },

    "5": {
        "label": "[?] Check Status of service",
        "func": getFullStatus
    },

    "6": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}


confMenu = {
    "1": {
        "label": "[?] Configure Ansible Vault",
        "func": vaultConfig
    },

    "2": {
        "label": "[?] Modify Service Playbook",
        "func": generatePkgPlaybook
    },

    "3": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}

deployMenu = {
    "1": {
        "label": "[^] Inmediate Deployment",
        "func": aptDeploy
    },

    "2": {
        "label": "[^] Automatic Deployment",
        "func": deployWatchdog
    },

    "3": {
        "label": "[Q] Back to Main",
        "func": lambda: None
    }
}