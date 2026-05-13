import os
import getpass
import subprocess

def vaultConfig():

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(CURRENT_DIR)

    vaultFile = os.path.join(root_dir, 'pass.yml')
    vaultPassFile = os.path.join(root_dir, '.vaultPass.txt')

    if not os.path.exists(vaultPassFile):
        aPass = getpass.getpass("Enter master password for Ansible Vault: ")
        with open(vaultPassFile, 'w') as f:
            f.write(aPass)
        os.chmod(vaultPassFile, 0o600)
        print(f"Created vault password file: {vaultPassFile}")

    if not os.path.exists(vaultFile):
        print(f"Creating new encrypted vault file: {vaultFile}")
        depPass = getpass.getpass("Enter the SUDO password for remote hosts: ")

        content = f"ansible_become_password: {depPass}\ninitial_device_password: {depPass}"

        cmd = [
            "ansible-vault", "encrypt",
            "--vault-password-file", vaultPassFile,
            "--output", vaultFile,
            "-"
        ]

        try:
            result = subprocess.run(
                cmd,
                input=content.encode(),
                capture_output=True,
                check=True
            )
            print("Vault file encrypted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating vault: {e.stderr.decode()}")
            if os.path.exists(vaultFile):
                os.remove(vaultFile)
