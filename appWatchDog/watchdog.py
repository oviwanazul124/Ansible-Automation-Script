#!/usr/bin/env python3

# Imports

import os
import json
import subprocess
import time
import sys

# Get the root folder for later usage and
# to make easier the imports of the utils.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Custom Imports

from utils.observability import loggingF
from utils.config_manager import configGet
from utils.sys_check import erHandler, checkPermission
from paths import *

# Path of the deployed hosts file
# This file will be used to keep track of the hosts active on the network and modified

stateFile = os.path.join(root_dir, "deployed_hosts.txt")


# getDeployedHosts function
# Objetive: This function is responsible for reading and creating
# the deployed_hosts.txt file.
def getDeployedHosts():

	if not os.path.exists(stateFile):

		loggingF(1, 'File deployed_hosts.txt not found. Trying to create it...')
		
		try:
			
			with open(stateFile, "w") as f:
				
				loggingF(1, 'File deployed_hosts.txt created')
				
				return set()

		except Exception as e:

			erHandler(e)
	
	try:

		loggingF(1, 'Reading deployed_hosts.txt file...')

		with open(stateFile, "r") as f:
			return set(line.strip() for line in f)

	except Exception as e:

		erHandler(e)

# saveDeloyedHost function
# Objetive: This function is responsible for saving the new host
# on the deployed_hosts.txt file.

def saveDeployedHost(ip):

	try:

		loggingF(1, f'Saving {ip} to deployed_hosts.txt...')

		with open(stateFile, "a") as f:
			f.write(f"{ip}\n")
	
	except Exception as e:

		erHandler(e)



def playbookRun(playbook_path, ip, extra_args=[]):

	# Get inventory path and check permissions

	invPath = os.path.join(root_dir, "appInv", "getInv.py")

	checkPermission(invPath)

	# Get remote user

	remote_user = configGet('users', 'remote_user')

	# Get vault files paths

	vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')
	vaultFile = os.path.join(root_dir, "pass.yml")



	if not os.path.exists(os.path.join(root_dir, playbook_path)):
		loggingF(4, f"Error: Playbook no encontrado en {playbook_path}")
		return False

	# CMD command for execution of the playbook

	command = [
		"ansible-playbook",
		"-i", invPath,
		os.path.join(root_dir, playbook_path),
		"-u", remote_user,
		"--limit", ip,
	] + extra_args

	# Add vault files if they exist

	if os.path.exists(vaultFile):
		command.extend(["-e", f"@{vaultFile}"])

	if os.path.exists(vaultPassFile):
		command.append(f"--vault-password-file={vaultPassFile}")

	# Create environment variable to disabled host key checking

	env = os.environ.copy()
	env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

	# Execute the command and handle errors	

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

	# Get SSH Key deployment playbook path

	ssh_playbook = os.path.join("playbooks", "SSHDeploy.yml")

	# Get package deployment playbook path

	pkg_playbook = os.path.join("playbooks", "InstallPackages.yml")

	# Get inventory path

	invPath = os.path.join(root_dir, "appInv", "getInv.py")

	checkPermission(invPath)

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

			loggingF(1, f"Host in inventory: {len(currentInv)}")

			for host in currentInv:

				if host not in deployed:

					loggingF(1, f"New host detected: {host}")

					try:
						if playbookRun(ssh_playbook, host, []):

							if playbookRun(pkg_playbook, host):

								loggingF(1, f"Guardando {host} en deployed_hosts.txt")
								
								saveDeployedHost(host)

					except Exception as e:
						loggingF(4, f'Error deploying to {host}: {str(e)}')
				else:
					pass

		except Exception as e:
			loggingF(4, f"Error in monitor cycle: {str(e)}")

		time.sleep(500)

if __name__ == "__main__":
	monitorCycle()
