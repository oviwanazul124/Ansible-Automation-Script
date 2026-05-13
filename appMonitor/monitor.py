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
        with open(stateFile, "w") as f:
            pass
        return set()
    with open(stateFile, "r") as f:
        return set(line.strip() for line in f)

def saveDeployedHost(ip):
    with open(stateFile, "a") as f:
        f.write(f"{ip}\n")

def monitorCycle():
	loggingF(1, "Monitor Service Active...")

	current_dir = os.path.dirname(os.path.abspath(__file__))
	root_dir = os.path.abspath(os.path.join(current_dir, ".."))
	invPath = os.path.join(root_dir, "appInv", "getInv.py")
	stateFile = os.path.join(root_dir, "deployed_hosts.txt")

	while True:
		try:
			if not os.path.exists(stateFile):
				with open(stateFile, "w") as f: pass
				loggingF(1, f"Archivo {stateFile} creado porque no existía.")

			deployed = getDeployedHosts()

			res = subprocess.run(
				["ansible-inventory", "-i", invPath, "--list"],
				capture_output=True,
				text=True,
				timeout=60
			)

			if res.returncode != 0:
				loggingF(4, f"Ansible Error (stderr): {res.stderr}")
				continue

			inventory_data = json.loads(res.stdout)

			currentInv = inventory_data.get('ungrouped', {}).get('hosts', [])
			if not currentInv:
				currentInv = inventory_data.get('all', {}).get('hosts', [])

			loggingF(1, f"Inventario leído. Hosts encontrados: {len(currentInv)}")

			for host in currentInv:
				loggingF(1, f"Analizando host: {host}")
				if host not in deployed:
					loggingF(1, f"¡NUEVO HOST DETECTADO!: {host}")

					if playbookRun(ssh_playbook, host, ["-k"]):
						if playbookRun(pkg_playbook, host):
							loggingF(1, f"Guardando {host} en deployed_hosts.txt")
							saveDeployedHost(host)
						else:
							loggingF(4, f"Fallo en Package para {host}")
					else:
						loggingF(4, f"Fallo en SSH para {host}")
				else:
					loggingF(1, f"El host {host} ya estaba desplegado (omitido).")

		except Exception as e:
			loggingF(4, f"ERROR CRÍTICO en el ciclo: {str(e)}")

		time.sleep(10)

if __name__ == "__main__":
	monitorCycle()
