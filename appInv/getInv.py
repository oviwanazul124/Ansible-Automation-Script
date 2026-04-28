#!/usr/bin/env python3

# Imports
import json
import sys
import os
from scapy.all import ARP, Ether, srp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Custom Imports

from utils.configR.configR import configGet
from utils.logger.logger import loggingF
from utils.checkRoot.checkRoot import checkRoot

# Check if the script is run as root

checkRoot()

def discovery():

    # Variables and Packet Set up
    netRange = configGet('network', 'subnet')
    user = configGet('users', 'remote_user')

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/ARP(pdst=netRange)
    
    result = srp(packet, timeout=3, verbose=0, iface="enp0s8")[0]

    detectedIPs = [received.psrc for sent, received in result]

    inventory = {
        'all': {
            'hosts': detectedIPs,
            'vars': {
                'ansible_user': user,
            }
        },
        '_meta': {
            'hostvars': {}
        }
    }
    return inventory

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--list':
        print(json.dumps(discovery()))
    else:
        print(json.dumps({'all': {'hosts': []}}))