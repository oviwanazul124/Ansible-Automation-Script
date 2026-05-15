#!/usr/bin/env python3

# Imports

import json
import sys
import os
from scapy.all import ARP, Ether, srp

# Custom Imports

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.sys_check import *
from utils.config_manager import *
from utils.observability import *

# discovery function.
# Objetive: This function is responsible for discovering the hosts on the network and parsing it to
# JSON for Ansible.

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