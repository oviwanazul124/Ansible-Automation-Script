import os
import json
import subprocess
import time
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from utils.logger.logger import loggingF
from utils.configR.configR import configGet

stateFile = os.path.join(root_dir, "deployed_hosts.txt")

def getDeployedHosts():
	if not os.path.exists(stateFile):
		with open(stateFile, "w") as f:
			pass
		return set()
	with open(stateFile, "r") as f:
		return set(line.strip() for line in f)

def saveDeployedHost(ip):
	with open(stateFile, "a") as f:
		f.write(f"{ip}\n")

def playbookRun(playbook_path, ip, extra_args=[]):
	invPath = os.path.join(root_dir, "appInv", "getInv.py")
	remote_user = configGet('users', 'remote_user')
	vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')

	if not os.path.exists(os.path.join(root_dir, playbook_path)):
		loggingF(4, f"Error: Playbook no encontrado en {playbook_path}")
		return False

	command = [
		"ansible-playbook",
		"-i", invPath,
		os.path.join(root_dir, playbook_path),
		"-u", remote_user,
		"--limit", ip,
		"-vvv"
	] + extra_args

	if os.path.exists(vaultFile):
		command.extend(["-e", f"@{vaultFile}"])

	if os.path.exists(vaultPassFile):
		command.append(f"--vault-password-file={vaultPassFile}")

	env = os.environ.copy()
	env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

	try:
		result = subprocess.run(command, env=env, capture_output=True, text=True)
		if result.returncode != 0:

			error_msg = result.stderr.strip() or result.stdout.strip()

			loggingF(4, f"Ansible Playbook Error: {error_msg}")
		return result.returncode == 0
	except Exception as e:
		loggingF(4, f"Excepción ejecutando playbook: {str(e)}")
		return False

def monitorCycle():

	loggingF(1, "Monitor Service Active...")
	ssh_playbook = os.path.join("playbooks", "SSHDeploy.yml")
	pkg_playbook = os.path.join("playbooks", "InstallPackages.yml")
	invPath = os.path.join(root_dir, "appInv", "getInv.py")

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
				loggingF(4, f"Ansible Inventory Error: {res.stderr}")
				time.sleep(10)
				continue

			inventory_data = json.loads(res.stdout)
			currentInv = inventory_data.get('ungrouped', {}).get('hosts', [])
			if not currentInv:
				currentInv = inventory_data.get('all', {}).get('hosts', [])

			loggingF(1, f"Inventario leído. Hosts encontrados: {len(currentInv)}")

			for host in currentInv:
				if host not in deployed:
					loggingF(1, f"¡NUEVO HOST DETECTADO!: {host}")
					if playbookRun(ssh_playbook, host, []):
						if playbookRun(pkg_playbook, host):
							loggingF(1, f"Guardando {host} en deployed_hosts.txt")
							saveDeployedHost(host)
						else:
							loggingF(4, f"Fallo en Package para {host}")
					else:
						loggingF(4, f"Fallo en SSH para {host}")
				else:
					pass

		except Exception as e:
			loggingF(4, f"ERROR CRÍTICO en el ciclo: {str(e)}")

		time.sleep(10)

if __name__ == "__main__":
	monitorCycle()
