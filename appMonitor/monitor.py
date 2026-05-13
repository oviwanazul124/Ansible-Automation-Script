import os
import json
import subprocess
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger.logger import loggingF
from utils.configR.configR import configGet

stateFile = "deployed_hosts.txt"

def getDeployedHosts():
    if not os.path.exists(stateFile):
        return set()
    with open(stateFile, "r") as f:
        return set(line.strip() for line in f)

def saveDeployedHost(ip):
    with open(stateFile, "a") as f:
        f.write(f"{ip}\n")

def playbookRun(playbook_path, ip, extra_args=[]):
    invPath = os.path.join("appInv", "getInv.py")
    remote_user = configGet('users', 'remote_user')
    vaultPassFile = '.vaultPass.txt'

    command = [
        "ansible-playbook",
        "-i", invPath,
        playbook_path,
        "-u", remote_user,
        "--limit", ip,
        f"--vault-password-file={vaultPassFile}"
    ] + extra_args

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    result = subprocess.run(command, env=env)
    return result.returncode == 0

def monitorCycle():
    loggingF(1, "Monitor Service Active: Waiting for new hosts...")

    ssh_playbook = os.path.join("playbooks", "SSHDeploy.yml")
    pkg_playbook = os.path.join("playbooks", "InstallPackages.yml")

    while True:
        deployed = getDeployedHosts()

        invPath = os.path.join("appInv", "getInv.py")
        res = subprocess.run(["ansible-inventory", "-i", invPath, "--list"], capture_output=True, text=True)

        if res.returncode == 0:
            currentInv = json.loads(res.stdout).get('all', {}).get('hosts', [])

            for host in currentInv:
                if host not in deployed:
                    loggingF(1, f"New device {host} found. Initializing deployment...")

                    if playbookRun(ssh_playbook, host, ["-k"]):
                        loggingF(1, f"SSH Keys OK for {host}. Proceeding to package install.")

                        if playbookRun(pkg_playbook, host):
                            loggingF(1, f"Package installation successful for {host}")
                            save_deployed_host(host)
                        else:
                            loggingF(4, f"Package installation FAILED for {host}")
                    else:
                        loggingF(4, f"SSH Key deployment FAILED for {host}")

        time.sleep(300)

if __name__ == "__main__":
    monitorCycle()
