from utils.logger.logger import loggingF
from utils.configR.configR import configGet
from pathlib import Path

def getIP():

    path = configGet('paths', 'ansible_hosts')

    # Check if the file exists, if not create a log error and continue

    if not Path(path).exists():
        loggingF(4, "Ansible hosts file not found / or created")
        return set()

    # If file exists, 

    with open(path, 'r') as f:
        return {line.strip() for line in f if line.strip() and not line.startswith('[')}
    