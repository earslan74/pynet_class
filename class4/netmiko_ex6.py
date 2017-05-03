#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass






def main(): 
    password = getpass()
    rtr1 = {'device_type': 'cisco_ios', 'ip': '184.105.247.70', 'username': 'pyclass', 'password': password}
    rtr2 = {'device_type': 'cisco_ios', 'ip': '184.105.247.71', 'username': 'pyclass', 'password': password}
    srx1 = {'device_type': 'juniper', 'ip': '184.105.247.76', 'username': 'pyclass', 'password': password}
    
    device_list = [rtr1, rtr2, srx1]
    for device in device_list:
        net_conn = ConnectHandler(**device)
        output = net_conn.send_command("show arp")
        print "\n>>>>>>> Device {0} ARP Table <<<<<<<<".format(device['ip'])
        print output
        print ">>>>>>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<\n"
        net_conn.disconnect()   
 




if __name__ == "__main__":
    main()
