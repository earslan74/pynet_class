#!/usr/bin/env python
'''
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6


class CiscoDevice(object):
    def __init__(self, ip_addr, uname):
        self.ip = ip_addr
        self.uname = uname
        self.remote_conn = None
    def telnet_connect(self):
        '''
        Establish telnet connection
        '''
        try:
            self.remote_conn = telnetlib.Telnet(self.ip, TELNET_PORT, TELNET_TIMEOUT)
            return self.remote_conn
        except socket.timeout:
            sys.exit("Connection timed-out")
    def login(self, passw):
        '''
        Login to network device
        '''
        output = self.remote_conn.read_until("sername:", TELNET_TIMEOUT)
        self.remote_conn.write(self.uname + '\n')
        output += self.remote_conn.read_until("ssword:", TELNET_TIMEOUT)
        self.remote_conn.write(passw + '\n')
        return output
    def send_command(self, cmd):
        '''
        Send a command down the telnet channel
        Return the response
        '''
        cmd = cmd.rstrip()
        self.remote_conn.write(cmd + '\n')
        time.sleep(1)
        return self.remote_conn.read_very_eager()
    def disable_paging(self, paging_cmd='terminal length 0'):
        '''
        Disable the paging of output (i.e. --More--)
        '''
        return self.send_command(paging_cmd)
    def disconnect(self):
        self.remote_conn.close()               

def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()
    rtr = CiscoDevice(ip_addr, username)
    rtr.telnet_connect()
    time.sleep(1)
    rtr.login(password)
    time.sleep(1)
    rtr.disable_paging()
    output = rtr.send_command("show ip int brief")

    print "\n\n"
    print output
    print "\n\n"

    rtr.disconnect()

if __name__ == "__main__":
    main()
