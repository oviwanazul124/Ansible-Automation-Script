import os
import subprocess
import getpass

def vaultConfig():
    vaultFile = 'pass.yml'
    vaultPassFile = '.vaultPass.txt'

    if not os.path.exists(vaultPassFile):
        aPass = getpass.getpass("Enter password for Ansible Vault: ")
        with open(vaultPassFile, 'w') as f:
            f.write(aPass)
        os.chmod(vaultPassFile, 0o600)
    
    if not os.path.exists(vaultFile):

        depPass = getpass.getpass("Enter password for the new vault file: ")

        content = f"initial_device_password: {depPass}"

        cmd = [
            "ansible-vault", "encrypt",
            "--vault-password-file", vaultPassFile,
            "--output", vaultFile,
            "-"
        ]

    subprocess.run(cmd, input=content.encode())