import os
import json
import subprocess
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger.logger import loggingF
from utils.configR.configR import configGet

stateFile = "deployed_hosts.txt"

def getDeployedHosts():
    if not os.path.exists(stateFile):
        return set()
    with open(stateFile, "r") as f:
        return set(line.strip() for line in f)

def saveDeployedHost(ip): # Asegúrate de que el nombre coincida abajo
    with open(stateFile, "a") as f:
        f.write(f"{ip}\n")

def monitorCycle():
    loggingF(1, "Monitor Service Active: Waiting for new hosts...")

    ssh_playbook = os.path.join("playbooks", "SSHDeploy.yml")
    pkg_playbook = os.path.join("playbooks", "InstallPackages.yml")
    invPath = os.path.join("appInv", "getInv.py")

    while True:
        try:
            deployed = getDeployedHosts()

            res = subprocess.run(
                ["ansible-inventory", "-i", invPath, "--list"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if res.returncode != 0:
                loggingF(4, f"Error obteniendo inventario: {res.stderr}")
            else:
                inventory_data = json.loads(res.stdout)
                currentInv = inventory_data.get('all', {}).get('hosts', [])

                for host in currentInv:
                    if host not in deployed:
                        loggingF(1, f"New device {host} found. Initializing...")

                        if playbookRun(ssh_playbook, host, ["-k"]):
                            if playbookRun(pkg_playbook, host):
                                loggingF(1, f"Success for {host}")
                                saveDeployedHost(host)
                            else:
                                loggingF(4, f"Package FAILED for {host}")
                        else:
                            loggingF(4, f"SSH FAILED for {host}")

        except subprocess.TimeoutExpired:
            loggingF(4, "Timeout: El inventario tardó demasiado en responder.")
        except Exception as e:
            loggingF(4, f"Error inesperado: {str(e)}")

        time.sleep(300)

if __name__ == "__main__":
    monitorCycle()
