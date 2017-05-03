#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass






def main(): 
    password = getpass()
 
    rtr1 = {'device_type': 'cisco_ios', 'ip': '184.105.247.70', 'username': 'pyclass', 'password': password}
    rtr2 = {'device_type': 'cisco_ios', 'ip': '184.105.247.71', 'username': 'pyclass', 'password': password}

    device_list = [rtr1, rtr2]

    for device in device_list:
        net_conn = ConnectHandler(**device)
        net_conn.config_mode()
        net_conn.send_config_from_file(config_file='conf_change.txt')
        net_conn.exit_config_mode()
        output = net_conn.send_command("show run | inc logging")
        print "\n>>>>>>>>Device {0} Logging Config <<<<<<<<<<<"
        print output
        print ">>>>>>>>>>>>>>>>>>> End <<<<<<<<<<<<<<<<<<<<<<<\n" 
        net_conn.disconnect()






if __name__ == "__main__":
    main()
