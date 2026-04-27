# Imports

from utils.configR.configR import configGet
from scapy.all import ARP, Ether, srp
from utils.getIP.getIP import getIP
from utils.logger.logger import loggingF
from utils.checkRoot.checkRoot import checkRoot
import subprocess

# Check if the script is run as root

checkRoot()

def discovery():

    # Variables and Packet Set up
    hostsPath = configGet('paths', 'ansible_hosts')
    netRange = configGet('network', 'subnet')
    vault_file = configGet('vault', 'vault_file')
    vault_pass_path = configGet('vault', 'vault_pass_path')
    ssh_pub_key = configGet('SSH', 'ssh_pub_key')
    user = configGet('users', 'remote_user')

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/ARP(pdst=netRange)
    
    result = srp(packet, timeout=3, verbose=0, iface="enp0s8")[0]

    detectedIPs = [received.psrc for sent, received in result]
    oldIPs = getIP()

    newIPs = [ip for ip in detectedIPs if ip not in oldIPs]

    # Create string for ansible process limit

    newIPsString = ",".join(newIPs) + ","

    # If there are no new IPs, log it and end

    if not newIPs:
        loggingF(2, "New devices wasn't detected.")
        return

    # If there is at least one new IP, log it and add it to the path
    
    with open(hostsPath, "a") as f:
        for ip in newIPs:
            f.write(f"\n{ip}")
            loggingF(2, f"Adding {ip} to the inventory")

    # Define the ansible process for installing devices

    ansibleProcess = (
        f"ansible all -i {hostsPath} --limit {newIPsString}"
        f" -m authorized_key -a \"user={user} key='{{{{ lookup('file', '{ssh_pub_key}') }}}}'\" "
        f"--extra-vars \"@{vault_file}\" "
        f"--vault-password-file {vault_pass_path} "
        f"-e \"ansible_ssh_pass={{{{ my_ssh_password }}}}\""        
    )
    
    # Try to deploy keys

    try:
        subprocess.run(ansibleProcess, shell=True, check=True)
        loggingF(2, f"Processed ended with success. {len(newIPs)} were added.")
    except subprocess.CalledProcessError as e:
        loggingF(4, f"An error ocurred while deploying the keys: {e}")


if __name__ == "__main__":
    discovery()