from pathlib import Path

# projectRoot function
# Objetive: Get the root path of the project.
# To ease the imports and use.

def projectRoot() -> Path:
    return Path(__file__).resolve().parents[1]

# Project Root

root_dir = projectRoot()

# Working paths

logsDir_path = root_dir / "logs"

inv_path = root_dir / "appInv" / "getInv.py"

sshPlaybook_path = root_dir / "playbooks" / "SSHDeploy.yml"

playbook_dir = root_dir / "playbooks"

playbook_path = root_dir / playbook_dir / "InstallPackages.yml"

aptPlaybook_path = root_dir / playbook_dir / "AppInstall.yml"  

script_path = root_dir / "appWatchDog" / "watchdog.py"

stateFile_path = root_dir / "deployed_hosts.txt"

logs_dir = root_dir / "logs" / "log.log"

config_path = root_dir / "config.ini"

vault_file_path = projectRoot() / "pass.yml"

vault_pass_file_path = projectRoot() / ".vaultPass.txt"

# Global Variables

serviceName = 'watchdog-Ansible'

dependencies = ["scapy", "pyyaml"]