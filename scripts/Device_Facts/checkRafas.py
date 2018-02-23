#!/usr/bin/env python
import napalm
import sys
import os
from devicecred import *
from prettytable import PrettyTable

#This defines the Header of the table that will be generated with printDevices 
table = PrettyTable([ 'Hostname', 'Vendor', 'Model', 'Serial Number', 'OS Version'])

#This sections loops the file that has the list of devices hostname/addresses and the
#the device types. The hostname and device type are split by whitespace assigned to
#ip_addr and platform. Device logins are imported from devicecred.py which has to
#be in the same directory, these details are used 
def openFile():
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, platform = line.strip().split()
            driver = napalm.get_network_driver(platform)
            dev = driver(username=username, password=password,  hostname=ip_addr)
            printDevices(dev)

def printDevices(dev):
    #Open Connection Devices
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
    table.add_row([ hostname, vendor , model , sn , os ])

    # Close the session with the device.
    dev.close()

#This runs openFile() and prints out the table and rows that have been collected
#in printDevices(dev)
def main():
    openFile()
    print(table)

#If there isn't a second file given an error will be thrown out
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to a ')
        sys.exit(1)
    main()