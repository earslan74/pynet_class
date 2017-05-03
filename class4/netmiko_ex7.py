#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass






def main(): 
    password = getpass()
    while True:
        buffer_size = raw_input("Enter the buffer size (4096 - 65000): ")
        if int(buffer_size) >= 4096 and int(buffer_size) <= 65000:
            break
        else:
            print "Incorrect buffer size! Try again."
            continue
 
    rtr2 = {'device_type': 'cisco_ios', 'ip': '184.105.247.71', 'username': 'pyclass', 'password': password}

    rtr2_conn = ConnectHandler(**rtr2)
    rtr2_conn.config_mode()
    rtr2_conn.send_command("logging buffered " + buffer_size)
    rtr2_conn.exit_config_mode()
    output = rtr2_conn.send_command("show run | inc logging buff")
    print "New Buffer size: {0}".format(buffer_size)
    print output
    rtr2_conn.disconnect()






if __name__ == "__main__":
    main()
