from appAptDeploy.aptDeploy import aptDeploy
from appSHHDeploy.sshDeploy import sshDeploy
from utils.dependenciesInstaller.depenInst import install_dependencies
from utils.getIP.getIP import inv

menuMain = {
    "1": {
        "label": "Install Required Packages",
        "func": lambda: aptDeploy(input("Enter the packages to install as example nginx, git:"))
    },
    "2": {
        "label": "Enter Debug Menu",
        "func": "debugMenu"
    },
    "3": {
        "label": "Enter Configuration Menu",
        "func": "confMenu"
    },
    "4": {
        "label": "Exit",
        "func": lambda: None
    }
}

debugMenu = {
    "1": {
        "label": "Check devices actives in the network",
        "func": inv
    },

    "2": {
        "label": "Back to Main",
        "func": lambda: None
    }
}


confMenu = {
    "1": {
        "label": "Deploy SSH Key",
        "func": sshDeploy
    },

    "2": {
        "label": "Install Dependencies",
        "func": lambda: install_dependencies()
    },

    "3": {
        "label": "Back to Main",
        "func": lambda: None
    }
}