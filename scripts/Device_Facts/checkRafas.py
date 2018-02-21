#!/usr/bin/env python
import napalm
import sys
import os
from devicecred import *
from prettytable import PrettyTable

with open(sys.argv[1]) as f:
    for line in f:
        ip_addr, platform = line.strip().split()

driver = napalm.get_network_driver(platform)

dev = driver(username=username,
             optional_args={
                 'use_keys': True,
                 'key_file': path, 
             },
             hostname=ip_addr,)

def main(devices):
    #Open Connection Devices
    print('Opening Connection')
    dev.open()

    #Using get_facts getter the device(s): Hostname, Vender, Serial
    #Number and Model will be collected
    vendor = dev.get_facts()['vendor']
    model = dev.get_facts()['model']
    sn = dev.get_facts()['serial_number']
    hostname = dev.get_facts()['hostname']
    os = dev.get_facts()['os_version']
    
    #Using the PrettyTable Module, this will create a table and  
    #be populated with the variables collected from get_facts
    t = PrettyTable([ 'Hostname', 'Vendor', 'Model', 'Serial Number', 'OS Version'])
    t.add_row([ hostname, vendor , model , sn , os ])
    print(t)

    # Close the session with the device.
    print('Close Connection')
    dev.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to a ')
        sys.exit(1)
    devices = sys.argv[1]
    main(devices)