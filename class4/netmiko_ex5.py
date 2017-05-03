#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass











def main(): 
    password = getpass()
    rtr2 = {'device_type': 'cisco_ios', 'ip': '184.105.247.71', 'username': 'pyclass', 'password': password}
    rtr2_conn = ConnectHandler(**rtr2)
    rtr2_conn.config_mode()
    print rtr2_conn.find_prompt()
    if rtr2_conn.check_config_mode:
        print "In Config Mode."
    else:
        print "Not in Config Mode."
    rtr2_conn.disconnect()






if __name__ == "__main__":
    main()
